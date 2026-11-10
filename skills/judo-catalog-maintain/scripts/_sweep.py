"""Shared helpers for the sweep scripts (design D10, D10a, D10b).

Work folder: target/sweep/<project>/<short-sha>/  (gitignored; never committed: it holds client names and code).
  src/          source worktree, detached at the swept SHA, never modified
  bp/           blueprint worktree on branch sweep/<project>-<short-sha>
  state.json    plan + step status (resume state)
  shape.md domain.md access.md counts.txt custom.md   overviews
  lanes/<lane>.json candidates.json decisions.json      subagent outputs
Hard rule: nothing here pushes, fetches into, or writes to any remote. Origin is read-only.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills" / "_lib"))
SWEEP = ROOT / "target" / "sweep"
LANES = ("model", "backend", "frontend", "schema")


def die(msg, code=2):
    print(msg, file=sys.stderr)
    sys.exit(code)


def git(args, cwd, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        die(f"git {' '.join(args)} failed in {cwd}: {r.stderr.strip()}")
    return r.stdout.strip()


def registry():
    sys.path.insert(0, str(ROOT / "skills" / "judo-catalog-maintain" / "scripts"))
    import projects  # noqa: E402
    rows, errs = projects.parse((ROOT / "PROJECTS.md").read_text())
    return {r["Project"]: r for r in rows}


def work_dir(project, sha):
    return SWEEP / project / sha[:7]


def load_state(w):
    p = w / "state.json"
    return json.loads(p.read_text()) if p.exists() else {}


def save_state(w, st):
    w.mkdir(parents=True, exist_ok=True)
    (w / "state.json").write_text(json.dumps(st, indent=1) + "\n")


def latest_work_dir(project):
    d = SWEEP / project
    if not d.exists():
        die(f"no sweep work folder for {project}; run sweep-prepare first")
    ws = sorted((p for p in d.iterdir() if (p / "state.json").exists()), key=lambda p: p.stat().st_mtime)
    if not ws:
        die(f"no prepared sweep for {project}")
    return ws[-1]


def cli(args, model, cwd):
    """Run the JUDO CLI read-only on a COPY of the source model (never the worktree file)."""
    from judo_common import cli_jar  # type: ignore
    env = dict(os.environ, JAVA_TOOL_OPTIONS=os.environ.get("JAVA_TOOL_OPTIONS", "-Xmx1g -XX:+UseSerialGC"))
    r = subprocess.run(["java", "-jar", str(cli_jar()), "-q", "-m", str(model), *args],
                       cwd=cwd, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout, r.stderr


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
