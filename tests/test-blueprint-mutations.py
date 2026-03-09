#!/usr/bin/env python3
"""Validate blueprint mutations against a Sandbox model using judo-cli.

Uses **server reuse** for speed: the CLI auto-starts a JVM server on the first
call and subsequent calls reuse it (~0.1s each vs ~2s cold start).

For each blueprint .md file:
  1. Extracts all GraphQL mutation code blocks
  2. Substitutes {{PLACEHOLDER}} tokens with Sandbox-compatible values
  3. Runs each mutation via judo-cli graphql (server stays warm)
  4. Runs judo-cli discard --force to reset the model to its original state
  5. Reports pass/fail per blueprint

The original tests/fixtures/Sandbox.model is NEVER modified — discard --force
reloads from the original file and clears all in-memory changes.

Exit code 0 = all blueprints pass, 1 = at least one failure, 2 = setup error.

Usage:
  python3 tests/test-blueprint-mutations.py                      # test all
  python3 tests/test-blueprint-mutations.py --blueprint <id>     # test one
  python3 tests/test-blueprint-mutations.py --json               # JSON output
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time

# ---- Configuration ----

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BLUEPRINTS_DIR = os.path.join(PROJECT_ROOT, "model-blueprints")
SANDBOX_MODEL = os.path.join(SCRIPT_DIR, "fixtures", "Sandbox.model")

# CLI jar: look in .claude/ first, then fall back to JUDO_CLI_JAR env var
_DEFAULT_CLI = os.path.join(PROJECT_ROOT, ".claude", "judo-cli.jar")
JUDO_CLI_JAR = os.environ.get("JUDO_CLI_JAR", _DEFAULT_CLI)

# Timeout per CLI invocation (seconds)
CLI_TIMEOUT = 60

# ---- Placeholder substitution ----

# Ordered: more specific patterns first so they match before generic ones.
PLACEHOLDERS = {
    "{{TYPES_NAMESPACE}}": "Sandbox::types",
    "{{MEASURES_NAMESPACE}}": "Sandbox::measures",
    "{{NAMESPACE}}": "Sandbox",
}

# For any remaining {{FOO}} tokens we auto-generate safe values.
_AUTO_COUNTER = 0


def _next_auto():
    global _AUTO_COUNTER
    _AUTO_COUNTER += 1
    return _AUTO_COUNTER


def substitute_placeholders(mutation: str) -> str:
    """Replace {{...}} placeholders with Sandbox-compatible values."""
    result = mutation
    for key, val in PLACEHOLDERS.items():
        result = result.replace(key, val)

    # Auto-substitute remaining tokens
    remaining = list(set(re.findall(r"\{\{([A-Z_0-9]+)\}\}", result)))
    for token in sorted(remaining):
        tag = "{{" + token + "}}"
        if "ORDINAL" in token or "COUNT" in token or "BOUND" in token:
            result = result.replace(tag, str(_next_auto()))
        elif "FQN" in token or "NAMESPACE" in token:
            result = result.replace(tag, "Sandbox")
        else:
            # Name-like placeholder
            safe_name = "Test" + token.title().replace("_", "")[:20]
            result = result.replace(tag, safe_name)
    return result


# ---- Mutation extraction ----

MUTATION_PATTERN = re.compile(
    r"```graphql\s*\n(mutation\s*\{.*?\})\s*\n```", re.DOTALL
)


def extract_mutations(md_path: str) -> list[str]:
    """Return all GraphQL mutation blocks from a blueprint markdown file."""
    with open(md_path) as f:
        content = f.read()
    return MUTATION_PATTERN.findall(content)


# ---- CLI helpers ----


def run_cli(model_path: str, *args: str) -> subprocess.CompletedProcess:
    """Run a judo-cli command. Uses -q (quiet) to suppress log noise."""
    cmd = ["java", "-jar", JUDO_CLI_JAR, "-m", model_path, "-q"] + list(args)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=CLI_TIMEOUT,
    )


def _extract_json_block(output: str) -> dict | None:
    """Find and parse the JSON object in CLI output (skip [INFO]/[WARN] lines)."""
    # Find the first '{' that starts a JSON block
    brace_start = output.find("{\n")
    if brace_start == -1:
        brace_start = output.find("{")
    if brace_start == -1:
        return None
    # Find matching closing brace by counting
    depth = 0
    for i in range(brace_start, len(output)):
        if output[i] == "{":
            depth += 1
        elif output[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(output[brace_start : i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def _extract_error_message(output: str) -> str:
    """Pull a concise error string from CLI output."""
    data = _extract_json_block(output)
    if data:
        # GraphQL-level errors array
        if "errors" in data and data["errors"]:
            return data["errors"][0].get("message", "unknown error")
        # Mutation-level result
        cr = (data.get("data") or {}).get("create") or {}
        if cr.get("errors"):
            msgs = [e.get("message", "") for e in cr["errors"]]
            return "; ".join(msgs) or "mutation errors"
        if cr.get("message"):
            return cr["message"]
        if cr.get("success") is False:
            fqn = cr.get("fqn", "")
            return f"Mutation failed (container or target not found, fqn={fqn!r})"

    # Fallback: grep for obvious error lines
    for line in output.splitlines():
        if "[ERROR]" in line:
            return line.strip()
    return "unknown error"


def run_mutation(model_path: str, mutation: str) -> tuple[bool, str, str]:
    """Execute a single GraphQL mutation. Returns (success, raw_output, error_msg)."""
    try:
        proc = run_cli(model_path, "graphql", mutation)
        output = proc.stdout + proc.stderr

        # Explicit failure: "success" : false
        if '"success" : false' in output or '"success":false' in output:
            return False, output, _extract_error_message(output)

        # Explicit success
        if '"success" : true' in output or '"success":true' in output:
            return True, output, ""

        # GraphQL-level errors (data: null)
        if '"errors"' in output:
            return False, output, _extract_error_message(output)

        # Non-zero exit
        if proc.returncode != 0:
            return False, output, _extract_error_message(output)

        # No recognizable success/fail pattern — treat as failure
        return False, output, "No success indicator in response"
    except subprocess.TimeoutExpired:
        return False, "", f"TIMEOUT after {CLI_TIMEOUT}s"
    except Exception as exc:
        return False, "", str(exc)


def discard_changes(model_path: str) -> bool:
    """Discard all in-memory changes — reloads the model from its original file.

    Returns True if discard succeeded, False otherwise.
    """
    try:
        proc = run_cli(model_path, "discard", "--force")
        return proc.returncode == 0
    except Exception:
        return False


# ---- Per-blueprint test ----


def test_blueprint(md_path: str, model_path: str) -> dict:
    """Test all mutations in a single blueprint.

    Uses the shared model_path (with server reuse). After testing, runs
    discard --force to reset the model to its original state.
    """
    global _AUTO_COUNTER
    _AUTO_COUNTER = 0  # reset per blueprint

    blueprint_id = os.path.basename(os.path.dirname(md_path))
    mutations = extract_mutations(md_path)

    if not mutations:
        return {
            "blueprint": blueprint_id,
            "status": "SKIP",
            "reason": "No mutation blocks found",
            "total": 0,
            "passed": 0,
            "failed": 0,
            "failures": [],
        }

    result = {
        "blueprint": blueprint_id,
        "total": len(mutations),
        "passed": 0,
        "failed": 0,
        "failures": [],
    }

    for idx, raw in enumerate(mutations, 1):
        substituted = substitute_placeholders(raw)
        ok, output, err_msg = run_mutation(model_path, substituted)
        if ok:
            result["passed"] += 1
        else:
            result["failed"] += 1
            result["failures"].append(
                {
                    "index": idx,
                    "raw": raw[:200],
                    "substituted": substituted[:200],
                    "error": err_msg[:300],
                }
            )

    result["status"] = "PASS" if result["failed"] == 0 else "FAIL"

    # Reset model to original state for next blueprint (server stays warm)
    discard_changes(model_path)

    return result


# ---- Main ----


def main():
    parser = argparse.ArgumentParser(description="Test blueprint mutations")
    parser.add_argument(
        "--blueprint",
        help="Test a single blueprint by ID (filename without .md)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    args = parser.parse_args()

    # Preflight checks
    if not os.path.exists(JUDO_CLI_JAR):
        print(
            f"ERROR: judo-cli.jar not found at {JUDO_CLI_JAR}\n"
            "Set JUDO_CLI_JAR env var or run: mvn validate -P download-model-cli",
            file=sys.stderr,
        )
        sys.exit(2)

    if not os.path.exists(SANDBOX_MODEL):
        print(
            f"ERROR: Sandbox model not found at {SANDBOX_MODEL}",
            file=sys.stderr,
        )
        sys.exit(2)

    # Collect blueprints (directory-based: model-blueprints/<id>/model.md)
    if args.blueprint:
        md = os.path.join(BLUEPRINTS_DIR, args.blueprint, "model.md")
        if not os.path.exists(md):
            print(f"ERROR: Blueprint not found: {md}", file=sys.stderr)
            sys.exit(2)
        files = [md]
    else:
        files = sorted(glob.glob(os.path.join(BLUEPRINTS_DIR, "*", "model.md")))

    if not files:
        print("No blueprint files found.", file=sys.stderr)
        sys.exit(2)

    # Run tests — all blueprints share the same model path (server reuse)
    model_path = SANDBOX_MODEL
    results = []
    start_time = time.time()

    for md_path in files:
        bp_id = os.path.basename(os.path.dirname(md_path))
        if not args.json:
            print(f"Testing: {bp_id}...", end=" ", flush=True)

        r = test_blueprint(md_path, model_path)
        results.append(r)

        if not args.json:
            status = r["status"]
            p, t = r["passed"], r["total"]
            if status == "SKIP":
                print(f"SKIP ({r.get('reason', '')})")
            elif status == "PASS":
                print(f"PASS ({p}/{t})")
            else:
                print(f"FAIL ({p}/{t})")
                for f in r["failures"]:
                    print(f"  #{f['index']}: {f['error'][:120]}")

    elapsed = time.time() - start_time

    # JSON output
    if args.json:
        print(json.dumps(results, indent=2))

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "SKIP")

    stream = sys.stderr if args.json else sys.stdout
    print(
        f"\n{'='*60}\n"
        f"SUMMARY: {total} blueprints | {passed} PASS | {failed} FAIL | {skipped} SKIP\n"
        f"Elapsed: {elapsed:.1f}s\n"
        f"{'='*60}",
        file=stream,
    )

    if failed > 0:
        if not args.json:
            print("\nFailed blueprints:")
            for r in results:
                if r["status"] == "FAIL":
                    print(f"  - {r['blueprint']}: {r['passed']}/{r['total']} mutations passed")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
