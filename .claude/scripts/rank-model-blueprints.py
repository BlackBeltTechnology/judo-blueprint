#!/usr/bin/env python3
"""
Model Blueprint Ranking Script

Reads all blueprint files from model-blueprints/*.md, parses their YAML
frontmatter, and ranks them by usage_count (how many projects use the fragment).

Usage:
  python3 rank-model-blueprints.py                  # Rank all blueprints
  python3 rank-model-blueprints.py --top 10          # Show top 10
  python3 rank-model-blueprints.py --min-uses 3      # Only show fragments in 3+ projects
  python3 rank-model-blueprints.py --summary          # Show summary statistics
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None

    yaml_text = match.group(1)
    meta = {}
    current_list = None

    for line in yaml_text.split("\n"):
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#"):
            continue

        if line_stripped.startswith("- ") and current_list is not None:
            val = line_stripped[2:].strip().strip('"').strip("'")
            meta[current_list].append(val)
            continue

        kv_match = re.match(r"^(\w+):\s*(.*)", line_stripped)
        if kv_match:
            key = kv_match.group(1)
            value = kv_match.group(2).strip().strip('"').strip("'")

            if value == "":
                meta[key] = []
                current_list = key
            else:
                if re.match(r"^\d+$", value):
                    meta[key] = int(value)
                elif re.match(r"^\d+\.\d+$", value):
                    meta[key] = float(value)
                else:
                    meta[key] = value
                current_list = None

    meta["_filepath"] = str(filepath)
    return meta


def scan_blueprints(base_dir):
    """Scan model-blueprints/<id>/BLUEPRINT.md and return all blueprint metadata."""
    blueprints_dir = os.path.join(base_dir, "model-blueprints")
    if not os.path.isdir(blueprints_dir):
        return []

    blueprints = []
    for entry in sorted(os.listdir(blueprints_dir)):
        subdir = os.path.join(blueprints_dir, entry)
        if not os.path.isdir(subdir):
            continue

        filepath = os.path.join(subdir, "BLUEPRINT.md")
        if not os.path.isfile(filepath):
            continue

        meta = parse_frontmatter(filepath)
        if meta:
            blueprints.append(meta)

    return blueprints


def print_table(blueprints, top_n=None, min_uses=None):
    """Print a formatted table of blueprints sorted by usage_count."""
    if min_uses:
        blueprints = [b for b in blueprints if b.get("usage_count", 0) >= min_uses]

    blueprints.sort(key=lambda b: b.get("usage_count", 0), reverse=True)

    if top_n:
        blueprints = blueprints[:top_n]

    if not blueprints:
        print("No model blueprints found.")
        return

    print(f"\n{'Rank':<5} {'Uses':<6} {'Title':<55} {'Projects'}")
    print("-" * 120)

    for i, bp in enumerate(blueprints, 1):
        projects = ", ".join(bp.get("projects", [])[:5])
        if len(bp.get("projects", [])) > 5:
            projects += f" (+{len(bp['projects']) - 5})"

        print(
            f"{i:<5} "
            f"{bp.get('usage_count', 0):<6} "
            f"{bp.get('title', bp.get('id', '?')):<55} "
            f"{projects}"
        )

    print(f"\nTotal: {len(blueprints)} blueprints")


def print_summary(blueprints):
    """Print summary statistics."""
    if not blueprints:
        print("No model blueprints found.")
        return

    usage_counts = [b.get("usage_count", 0) for b in blueprints]
    total = len(blueprints)
    total_uses = sum(usage_counts)
    max_uses = max(usage_counts)
    avg_uses = total_uses / total if total else 0

    multi_project = sum(1 for u in usage_counts if u > 1)
    single_project = sum(1 for u in usage_counts if u == 1)

    all_projects = set()
    for bp in blueprints:
        all_projects.update(bp.get("projects", []))

    print(f"\n=== Model Blueprint Summary ===")
    print(f"Total blueprints:       {total}")
    print(f"Total usage instances:  {total_uses}")
    print(f"Unique projects:        {len(all_projects)}")
    print(f"Max uses (single bp):   {max_uses}")
    print(f"Avg uses per blueprint: {avg_uses:.1f}")
    print(f"Multi-project (2+):     {multi_project}")
    print(f"Single-project:         {single_project}")

    # Distribution
    print(f"\nUsage Distribution:")
    for threshold in [5, 4, 3, 2, 1]:
        count = sum(1 for u in usage_counts if u >= threshold)
        print(f"  {threshold}+ projects: {count} blueprints")


def main():
    parser = argparse.ArgumentParser(description="Rank JUDO model blueprints by usage")
    parser.add_argument(
        "--top", type=int, default=None,
        help="Show only top N blueprints"
    )
    parser.add_argument(
        "--min-uses", type=int, default=None,
        help="Only show blueprints used in N+ projects"
    )
    parser.add_argument(
        "--summary", action="store_true",
        help="Show summary statistics"
    )
    parser.add_argument(
        "--base-dir", default=os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()),
        help="Base directory of the project"
    )

    args = parser.parse_args()
    blueprints = scan_blueprints(args.base_dir)

    if not blueprints:
        print("No model blueprint files found. Run /collect-model-blueprints first.")
        sys.exit(0)

    if args.summary:
        print_summary(blueprints)
    else:
        print_table(blueprints, top_n=args.top, min_uses=args.min_uses)


if __name__ == "__main__":
    if not sys.stdin.isatty():
        try:
            hook_input = json.load(sys.stdin)
            if "cwd" in hook_input:
                sys.argv.extend(["--base-dir", hook_input["cwd"]])
        except (json.JSONDecodeError, EOFError):
            pass
    main()
