#!/usr/bin/env python3
"""
Best Practice Scoring Script

Reads all best-practice files from best-practices/{model,backend,frontend}/*.md,
parses their YAML frontmatter, and calculates weighted scores based on:
- usage_count: how many projects use this pattern (weight: 10 per use)
- recency_bonus: newer projects give higher weight
- alternative_penalty: patterns with many alternatives score lower (-2 per alt)

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

# Project ordering from RESEARCH-TRACKER.md (index 1-26, later = newer = higher weight)
PROJECT_ORDER = {
    "trivia": 1,
    "rackinspect": 2,
    "itracker": 3,
    "skillmatrix-frontend": 4,
    "actiongroup-test-react": 5,
    "alba": 6,
    "skillmatrix-model": 7,
    "mlszksz-platform": 8,
    "viterra_demo": 9,
    "kozut-eugyfel-client": 10,
    "bhs-global-operation": 11,
    "mjsz": 13,
    "judo-demo-miniworkflow": 14,
    "ubives": 15,
    "ams-model": 16,
    "sanctuary-backend": 17,
    "park-here": 18,
    "indamedia-adtrack": 19,
    "InterfaceRegister": 20,
    "judo-partner": 21,
    "kozut-eugyfel-model-test": 22,
    "workflow-poc": 23,
    "reserve-app": 24,
    "doors-model": 25,
    "ams-frontend": 26,
}

TOTAL_PROJECTS = len(PROJECT_ORDER)
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


def calculate_score(meta):
    """Calculate weighted score for a best practice."""
    usage_count = meta.get("usage_count", 0)
    alternative_count = meta.get("alternative_count", 0)
    projects = meta.get("projects", [])

    # Base score from usage
    base_score = usage_count * 10

    # Recency bonus: newer projects (higher index) give more weight
    recency_bonus = 0.0
    for proj in projects:
        proj_index = PROJECT_ORDER.get(proj, 0)
        if proj_index > 0:
            recency_bonus += (proj_index / TOTAL_PROJECTS) * 10

    # Alternative penalty
    alternative_penalty = alternative_count * 2

    score = base_score + recency_bonus - alternative_penalty
    return round(score, 1)


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

    domains = [args.domain] if args.domain else None
    best_practices = scan_best_practices(args.base_dir, domains)

    if not best_practices:
        print("No best-practice files found. Run the best-practice collector agents first.")
        sys.exit(0)

    # Recalculate scores
    for bp in best_practices:
        bp["score"] = calculate_score(bp)

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
