"""Shared script contract for judo-blueprint skills (design D5).

Every script: runs from any cwd, `--help`, `--json`, non-zero exit on failure.
CLI resolution: $JUDO_CLI_JAR, then <repo>/target/judo-cli.jar, then an error
with the download command.
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys

LIB = pathlib.Path(__file__).resolve().parent


def repo_root() -> pathlib.Path:
    """The judo-blueprint checkout this script lives in (skills/_lib/..)."""
    return LIB.parent.parent


def cli_jar() -> pathlib.Path:
    env = os.environ.get("JUDO_CLI_JAR")
    if env and pathlib.Path(env).is_file():
        return pathlib.Path(env)
    p = repo_root() / "target" / "judo-cli.jar"
    if p.is_file():
        return p
    die(f"JUDO CLI jar not found. Set JUDO_CLI_JAR or run: (cd {repo_root()} && ./mvnw -q validate -P download-model-cli)")


def cli_version() -> str:
    out = run_cli(["-V"], cwd=None, check=False).stdout.strip()
    return out.split()[-1] if out else "unknown"


def run_cli(args: list[str], cwd: str | os.PathLike | None, check: bool = True, model: str | None = None) -> subprocess.CompletedProcess:
    cmd = ["java", "-jar", str(cli_jar()), "-q"]
    if model:
        cmd += ["-m", str(model)]
    cmd += args
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        die(f"CLI failed ({' '.join(args)}):\n{r.stdout}\n{r.stderr}")
    return r


def die(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def emit(obj, as_json: bool, human: str = ""):
    if as_json:
        print(json.dumps(obj, indent=2, default=str))
    elif human:
        print(human)
