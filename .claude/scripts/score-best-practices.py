#!/usr/bin/env python3
"""
Best Practice Scoring Script

Reads all best-practice files from best-practices/{model,backend,frontend}/*.md,
parses their YAML frontmatter, and calculates scores normalized to 0-100:
- raw_score = usage_count * 10 + recency_bonus - alternative_penalty
- Normalized to 0-100 range across all patterns
- Project weights from PROJECTS.md act as proportional multipliers:
  weight 0 = 1.0x (neutral), +10 = 2.0x (double), -10 = 0x (zeroed)

Usage:
  python3 score-best-practices.py                    # Score all domains
  python3 score-best-practices.py --domain model     # Score only model domain
  python3 score-best-practices.py --update           # Update scores in best-practice files
  python3 score-best-practices.py --top 20           # Show top 20 patterns
  python3 score-best-practices.py --category entity  # Filter by category
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from _projects import parse_projects_md

DOMAINS = ["model", "backend", "frontend"]


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Match YAML frontmatter between --- delimiters
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None, content

    yaml_text = match.group(1)
    body = content[match.end():]
    meta = {}

    # Simple YAML parser for our known structure
    current_key = None
    current_list = None

    for line in yaml_text.split("\n"):
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#"):
            continue

        # List item
        if line_stripped.startswith("- ") and current_list is not None:
            val = line_stripped[2:].strip().strip('"').strip("'")
            meta[current_list].append(val)
            continue

        # Key-value pair
        kv_match = re.match(r"^(\w+):\s*(.*)", line_stripped)
        if kv_match:
            key = kv_match.group(1)
            value = kv_match.group(2).strip().strip('"').strip("'")

            if value == "":
                # Could be a list or empty value
                meta[key] = []
                current_list = key
                current_key = key
            else:
                # Convert numeric values
                if re.match(r"^\d+$", value):
                    meta[key] = int(value)
                elif re.match(r"^\d+\.\d+$", value):
                    meta[key] = float(value)
                else:
                    meta[key] = value
                current_list = None
                current_key = key

    return meta, body


def calculate_components(meta, project_order, project_weights, total_projects):
    """Calculate the three scoring components for a best practice.

    Returns (usage_raw, recency_raw, weight_norm):
      - usage_raw: usage_count minus alternative penalty (will be normalized)
      - recency_raw: average recency index across projects (will be normalized)
      - weight_norm: max project weight mapped to 0-100 directly
    """
    projects = meta.get("projects", [])
    alternative_count = meta.get("alternative_count", 0)
    usage_raw = meta.get("usage_count", 0) - alternative_count * 0.2

    recency_values = []
    for proj in projects:
        proj_index = project_order.get(proj, 0)
        if proj_index > 0:
            recency_values.append(proj_index / total_projects)
    recency_raw = sum(recency_values) / len(recency_values) if recency_values else 0

    # Weight: max across projects, map [-10,+10] to [0,100]
    # Using max (not average) so adding more projects never lowers the weight component.
    # The usage component already rewards having more projects.
    if projects:
        max_weight = max(project_weights.get(p, 0) for p in projects)
        max_weight = max(-10, min(10, max_weight))
        weight_norm = (max_weight + 10) / 20 * 100
    else:
        weight_norm = 50.0

    return usage_raw, recency_raw, weight_norm


# Component weights: weight has 60% influence, usage 20%, recency 20%
USAGE_WEIGHT = 0.20
RECENCY_WEIGHT = 0.20
PROJECT_WEIGHT = 0.60


def calculate_scores(best_practices, project_order, project_weights, total_projects):
    """Calculate final 0-100 scores using weighted combination of 3 components."""
    for bp in best_practices:
        usage_raw, recency_raw, weight_norm = calculate_components(
            bp, project_order, project_weights, total_projects
        )
        bp["_usage_raw"] = usage_raw
        bp["_recency_raw"] = recency_raw
        bp["_weight_norm"] = weight_norm

    usage_vals = [bp["_usage_raw"] for bp in best_practices]
    recency_vals = [bp["_recency_raw"] for bp in best_practices]

    usage_min, usage_max = min(usage_vals), max(usage_vals)
    recency_min, recency_max = min(recency_vals), max(recency_vals)

    for bp in best_practices:
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
    meta["last_updated"] = datetime.now().strftime("%Y-%m-%d")

    lines = ["---"]
    # Write scalar fields first
    scalar_keys = [
        "id", "title", "domain", "category", "score",
        "usage_count", "alternative_count", "first_seen", "last_updated"
    ]
    for key in scalar_keys:
        if key in meta:
            val = meta[key]
            if isinstance(val, str) and not re.match(r"^\d+\.?\d*$", val):
                lines.append(f'{key}: "{val}"')
            else:
                lines.append(f"{key}: {val}")

    # Write list fields
    list_keys = ["projects", "alternatives"]
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


def scan_best_practices(base_dir, domains=None):
    """Scan best-practice directories and return all pattern metadata."""
    if domains is None:
        domains = DOMAINS

    best_practices = []

    for domain in domains:
        domain_dir = os.path.join(base_dir, "best-practices", domain)
        if not os.path.isdir(domain_dir):
            continue

        for filename in sorted(os.listdir(domain_dir)):
            if not filename.endswith(".md") or filename == "INDEX.md":
                continue

            filepath = os.path.join(domain_dir, filename)
            meta, body = parse_frontmatter(filepath)

            if meta is None:
                print(f"  WARNING: No frontmatter in {filepath}", file=sys.stderr)
                continue

            meta["_filepath"] = filepath
            meta["_filename"] = filename
            meta["_body"] = body
            best_practices.append(meta)

    return best_practices


def print_table(best_practices, top_n=None, category_filter=None):
    """Print a formatted table of best practices sorted by score."""
    # Filter by category if specified
    if category_filter:
        best_practices = [b for b in best_practices if b.get("category") == category_filter]

    # Sort by score descending
    best_practices.sort(key=lambda b: b.get("score", 0), reverse=True)

    # Limit results
    if top_n:
        best_practices = best_practices[:top_n]

    if not best_practices:
        print("No best practices found.")
        return

    # Print header
    print(f"\n{'Rank':<5} {'Score':<7} {'Uses':<5} {'Alts':<5} {'Domain':<10} {'Category':<14} {'Title':<50} {'Projects'}")
    print("-" * 140)

    for i, bp in enumerate(best_practices, 1):
        projects = ", ".join(bp.get("projects", [])[:5])
        if len(bp.get("projects", [])) > 5:
            projects += f" (+{len(bp['projects']) - 5})"

        print(
            f"{i:<5} "
            f"{bp.get('score', 0):<7} "
            f"{bp.get('usage_count', 0):<5} "
            f"{bp.get('alternative_count', 0):<5} "
            f"{bp.get('domain', '?'):<10} "
            f"{bp.get('category', '?'):<14} "
            f"{bp.get('title', bp.get('id', '?')):<50} "
            f"{projects}"
        )

    print(f"\nTotal: {len(best_practices)} patterns")


def print_summary(best_practices):
    """Print domain and category summary statistics."""
    domain_counts = {}
    category_counts = {}
    total_score = 0

    for bp in best_practices:
        domain = bp.get("domain", "unknown")
        category = bp.get("category", "unknown")
        score = bp.get("score", 0)

        domain_counts[domain] = domain_counts.get(domain, 0) + 1
        key = f"{domain}/{category}"
        category_counts[key] = category_counts.get(key, 0) + 1
        total_score += score

    print(f"\n=== Best Practice Summary ===")
    print(f"Total patterns: {len(best_practices)}")
    print(f"Total score: {total_score}")
    print(f"\nBy Domain:")
    for domain in sorted(domain_counts):
        print(f"  {domain}: {domain_counts[domain]} patterns")

    print(f"\nBy Category:")
    for cat in sorted(category_counts):
        print(f"  {cat}: {category_counts[cat]} patterns")


def main():
    parser = argparse.ArgumentParser(description="Score JUDO best-practice patterns")
    parser.add_argument(
        "--domain", choices=DOMAINS,
        help="Filter by domain (model, backend, frontend)"
    )
    parser.add_argument(
        "--update", action="store_true",
        help="Recalculate and write scores back to best-practice files"
    )
    parser.add_argument(
        "--top", type=int, default=None,
        help="Show only top N patterns"
    )
    parser.add_argument(
        "--category",
        help="Filter by category (e.g., entity, interceptor, hook)"
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

    # Read project order from PROJECTS.md (single source of truth)
    project_order, project_weights, total_projects = parse_projects_md(args.base_dir)
    if total_projects == 0:
        print("WARNING: Could not read PROJECTS.md, scores may be inaccurate.", file=sys.stderr)

    domains = [args.domain] if args.domain else None
    best_practices = scan_best_practices(args.base_dir, domains)

    if not best_practices:
        print("No best-practice files found. Run the best-practice collector agents first.")
        sys.exit(0)

    # Calculate scores: 3-component weighted combination (usage 20%, recency 20%, weight 60%)
    calculate_scores(best_practices, project_order, project_weights, total_projects)

    # Update files if requested
    if args.update:
        updated = 0
        for bp in best_practices:
            filepath = bp["_filepath"]
            body = bp["_body"]
            new_score = bp["score"]
            update_frontmatter(filepath, bp, body, new_score)
            updated += 1
        print(f"Updated scores in {updated} best-practice files.")

    # Print results
    if args.summary:
        print_summary(best_practices)
    else:
        print_table(best_practices, top_n=args.top, category_filter=args.category)


if __name__ == "__main__":
    # Support hook-style invocation via stdin (piped JSON input)
    if not sys.stdin.isatty():
        try:
            hook_input = json.load(sys.stdin)
            # If called as a hook, use cwd as base-dir
            if "cwd" in hook_input:
                sys.argv.extend(["--base-dir", hook_input["cwd"]])
        except (json.JSONDecodeError, EOFError):
            pass
    main()
