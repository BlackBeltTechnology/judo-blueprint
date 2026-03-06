#!/usr/bin/env python3
"""
Model Blueprint Scoring Script

Reads all blueprint files from model-blueprints/*.md, parses their YAML
frontmatter, and calculates weighted scores normalized to 0-100:
- raw_score = usage_count * 10 + recency_bonus
- Normalized to 0-100 range across all blueprints
- Project weights from PROJECTS.md act as proportional multipliers:
  weight 0 = 1.0x (neutral), +10 = 2.0x (double), -10 = 0x (zeroed)
  The average weight across a blueprint's projects determines the multiplier.

Usage:
  python3 score-model-blueprints.py                  # Score all blueprints
  python3 score-model-blueprints.py --update         # Write scores to files
  python3 score-model-blueprints.py --top 20         # Top N blueprints
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from _projects import parse_projects_md


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None, content

    yaml_text = match.group(1)
    body = content[match.end():]
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

    return meta, body


def calculate_components(meta, project_order, project_weights, total_projects):
    """Calculate the three scoring components for a blueprint.

    Returns (usage_raw, recency_raw, weight_norm):
      - usage_raw: usage_count (will be min-max normalized later)
      - recency_raw: average recency index across projects (will be normalized)
      - weight_norm: average project weight mapped to 0-100 directly
    """
    projects = meta.get("projects", [])
    usage_raw = meta.get("usage_count", 0)

    # Average recency across projects (0 to 1 range, will be normalized)
    recency_values = []
    for proj in projects:
        proj_index = project_order.get(proj, 0)
        if proj_index > 0:
            recency_values.append(proj_index / total_projects)
    recency_raw = sum(recency_values) / len(recency_values) if recency_values else 0

    # Weight: average across projects, map [-10,+10] to [0,100]
    if projects:
        weights = [project_weights.get(p, 0) for p in projects]
        avg_weight = sum(weights) / len(weights)
        avg_weight = max(-10, min(10, avg_weight))
        weight_norm = (avg_weight + 10) / 20 * 100  # -10→0, 0→50, +10→100
    else:
        weight_norm = 50.0  # neutral

    return usage_raw, recency_raw, weight_norm


# Component weights: weight has 60% influence, usage 20%, recency 20%
USAGE_WEIGHT = 0.20
RECENCY_WEIGHT = 0.20
PROJECT_WEIGHT = 0.60


def calculate_scores(blueprints, project_order, project_weights, total_projects):
    """Calculate final 0-100 scores using weighted combination of 3 components."""
    # First pass: compute raw components
    for bp in blueprints:
        usage_raw, recency_raw, weight_norm = calculate_components(
            bp, project_order, project_weights, total_projects
        )
        bp["_usage_raw"] = usage_raw
        bp["_recency_raw"] = recency_raw
        bp["_weight_norm"] = weight_norm

    # Min-max normalize usage and recency across all blueprints
    usage_vals = [bp["_usage_raw"] for bp in blueprints]
    recency_vals = [bp["_recency_raw"] for bp in blueprints]

    usage_min, usage_max = min(usage_vals), max(usage_vals)
    recency_min, recency_max = min(recency_vals), max(recency_vals)

    for bp in blueprints:
        if usage_max > usage_min:
            usage_norm = (bp["_usage_raw"] - usage_min) / (usage_max - usage_min) * 100
        else:
            usage_norm = 50.0

        if recency_max > recency_min:
            recency_norm = (bp["_recency_raw"] - recency_min) / (recency_max - recency_min) * 100
        else:
            recency_norm = 50.0

        final = (
            USAGE_WEIGHT * usage_norm
            + RECENCY_WEIGHT * recency_norm
            + PROJECT_WEIGHT * bp["_weight_norm"]
        )
        bp["score"] = round(max(0, min(100, final)), 1)


def update_frontmatter(filepath, meta, body, new_score):
    """Write updated frontmatter back to the file."""
    meta["score"] = new_score

    lines = ["---"]
    # Write scalar fields first
    scalar_keys = [
        "id", "title", "score",
        "usage_count", "first_seen", "last_updated"
    ]
    for key in scalar_keys:
        if key in meta:
            val = meta[key]
            if isinstance(val, str) and not re.match(r"^\d+\.?\d*$", val):
                lines.append(f'{key}: "{val}"')
            else:
                lines.append(f"{key}: {val}")

    # Write list fields
    list_keys = ["projects"]
    for key in list_keys:
        if key in meta and isinstance(meta[key], list):
            if meta[key]:
                lines.append(f"{key}:")
                for item in meta[key]:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}:")

    lines.append("---")
    lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + body)


def scan_blueprints(base_dir):
    """Scan model-blueprints/ and return all blueprint metadata."""
    blueprints_dir = os.path.join(base_dir, "model-blueprints")
    if not os.path.isdir(blueprints_dir):
        return []

    blueprints = []
    skip_files = {"PROGRESS.md", "INDEX.md", "CONVENTIONS.md"}

    for filename in sorted(os.listdir(blueprints_dir)):
        if not filename.endswith(".md") or filename in skip_files:
            continue

        filepath = os.path.join(blueprints_dir, filename)
        meta, body = parse_frontmatter(filepath)

        if meta is None:
            print(f"  WARNING: No frontmatter in {filepath}", file=sys.stderr)
            continue

        meta["_filepath"] = filepath
        meta["_filename"] = filename
        meta["_body"] = body
        blueprints.append(meta)

    return blueprints


def print_table(blueprints, top_n=None):
    """Print a formatted table of blueprints sorted by score."""
    blueprints.sort(key=lambda b: b.get("score", 0), reverse=True)

    if top_n:
        blueprints = blueprints[:top_n]

    if not blueprints:
        print("No model blueprints found.")
        return

    print(f"\n{'Rank':<5} {'Score':<7} {'Uses':<5} {'Title':<55} {'Projects'}")
    print("-" * 130)

    for i, bp in enumerate(blueprints, 1):
        projects = ", ".join(bp.get("projects", [])[:5])
        if len(bp.get("projects", [])) > 5:
            projects += f" (+{len(bp['projects']) - 5})"

        print(
            f"{i:<5} "
            f"{bp.get('score', 0):<7} "
            f"{bp.get('usage_count', 0):<5} "
            f"{bp.get('title', bp.get('id', '?')):<55} "
            f"{projects}"
        )

    print(f"\nTotal: {len(blueprints)} blueprints")


def print_summary(blueprints):
    """Print summary statistics."""
    if not blueprints:
        print("No model blueprints found.")
        return

    scores = [b.get("score", 0) for b in blueprints]
    usage_counts = [b.get("usage_count", 0) for b in blueprints]
    total = len(blueprints)
    total_score = sum(scores)
    avg_score = total_score / total if total else 0

    all_projects = set()
    for bp in blueprints:
        all_projects.update(bp.get("projects", []))

    print(f"\n=== Model Blueprint Scoring Summary ===")
    print(f"Total blueprints:       {total}")
    print(f"Total score:            {total_score}")
    print(f"Average score:          {avg_score:.1f}")
    print(f"Unique projects:        {len(all_projects)}")
    print(f"Max uses (single bp):   {max(usage_counts)}")


def main():
    parser = argparse.ArgumentParser(description="Score JUDO model blueprints")
    parser.add_argument(
        "--update", action="store_true",
        help="Recalculate and write scores back to blueprint files"
    )
    parser.add_argument(
        "--top", type=int, default=None,
        help="Show only top N blueprints"
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

    # Read project data from PROJECTS.md
    project_order, project_weights, total_projects = parse_projects_md(args.base_dir)
    if total_projects == 0:
        print("WARNING: Could not read PROJECTS.md, scores may be inaccurate.", file=sys.stderr)

    blueprints = scan_blueprints(args.base_dir)

    if not blueprints:
        print("No model blueprint files found. Run /collect-model-blueprints first.")
        sys.exit(0)

    # Calculate scores: 3-component weighted combination (usage 20%, recency 20%, weight 60%)
    calculate_scores(blueprints, project_order, project_weights, total_projects)

    # Update files if requested
    if args.update:
        updated = 0
        for bp in blueprints:
            filepath = bp["_filepath"]
            body = bp["_body"]
            new_score = bp["score"]
            update_frontmatter(filepath, bp, body, new_score)
            updated += 1
        print(f"Updated scores in {updated} model blueprint files.")

    # Print results
    if args.summary:
        print_summary(blueprints)
    else:
        print_table(blueprints, top_n=args.top)


if __name__ == "__main__":
    if not sys.stdin.isatty():
        try:
            hook_input = json.load(sys.stdin)
            if "cwd" in hook_input:
                sys.argv.extend(["--base-dir", hook_input["cwd"]])
        except (json.JSONDecodeError, EOFError):
            pass
    main()
