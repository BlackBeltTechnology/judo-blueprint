#!/usr/bin/env python3
"""
Unified Catalog Query Script

Queries best-practices and model-blueprints catalogs with two modes:
  list     Show all items with just id, title, and score (compact for agent selection)
  get ID   Show the full content of a specific item by id

This allows agents to first see what exists (names + scores only), then selectively
read only the items relevant to the project they're analyzing.

Usage:
  python3 query-catalog.py list                              # All best-practices + blueprints
  python3 query-catalog.py list --type best-practice          # Only best-practices
  python3 query-catalog.py list --type blueprint              # Only blueprints
  python3 query-catalog.py list --domain model                # Only model-domain best-practices
  python3 query-catalog.py list --domain model --type all     # Model best-practices + blueprints
  python3 query-catalog.py list --category entity             # Filter by category
  python3 query-catalog.py get audit-log-entity               # Full content of one item
  python3 query-catalog.py get collection-lower-bound-zero    # Full content of one item
  python3 query-catalog.py get id1 id2 id3                    # Full content of multiple items
"""

import argparse
import os
import re
import sys


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file. Returns (meta_dict, full_content)."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None, content

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

    return meta, content


def scan_all(base_dir, type_filter=None, domain_filter=None, category_filter=None):
    """Scan both best-practices and model-blueprints. Returns list of (meta, filepath, item_type)."""
    items = []

    # Scan best-practices
    if type_filter in (None, "all", "best-practice", "bp"):
        for domain in ["model", "backend", "frontend"]:
            if domain_filter and domain != domain_filter:
                continue
            domain_dir = os.path.join(base_dir, "best-practices", domain)
            if not os.path.isdir(domain_dir):
                continue
            for filename in sorted(os.listdir(domain_dir)):
                if not filename.endswith(".md") or filename == "INDEX.md":
                    continue
                filepath = os.path.join(domain_dir, filename)
                meta, _ = parse_frontmatter(filepath)
                if meta:
                    items.append((meta, filepath, "best-practice"))

    # Scan model-blueprints
    if type_filter in (None, "all", "blueprint", "mb"):
        blueprints_dir = os.path.join(base_dir, "model-blueprints")
        if os.path.isdir(blueprints_dir):
            for filename in sorted(os.listdir(blueprints_dir)):
                if not filename.endswith(".md") or filename in ("PROGRESS.md", "INDEX.md"):
                    continue
                filepath = os.path.join(blueprints_dir, filename)
                meta, _ = parse_frontmatter(filepath)
                if meta:
                    items.append((meta, filepath, "blueprint"))

    # Apply category filter
    if category_filter:
        items = [(m, f, t) for m, f, t in items if m.get("category", "") == category_filter]

    return items


def find_by_id(base_dir, item_id):
    """Find a specific item by its id across all catalogs. Returns (filepath, full_content) or None."""
    # Check best-practices (all domains)
    for domain in ["model", "backend", "frontend"]:
        filepath = os.path.join(base_dir, "best-practices", domain, f"{item_id}.md")
        if os.path.isfile(filepath):
            meta, content = parse_frontmatter(filepath)
            if meta and meta.get("id") == item_id:
                return filepath, content

    # Check model-blueprints
    filepath = os.path.join(base_dir, "model-blueprints", f"{item_id}.md")
    if os.path.isfile(filepath):
        meta, content = parse_frontmatter(filepath)
        if meta and meta.get("id") == item_id:
            return filepath, content

    # Fallback: scan all files in case filename != id
    for domain in ["model", "backend", "frontend"]:
        domain_dir = os.path.join(base_dir, "best-practices", domain)
        if not os.path.isdir(domain_dir):
            continue
        for filename in os.listdir(domain_dir):
            if not filename.endswith(".md") or filename == "INDEX.md":
                continue
            filepath = os.path.join(domain_dir, filename)
            meta, content = parse_frontmatter(filepath)
            if meta and meta.get("id") == item_id:
                return filepath, content

    blueprints_dir = os.path.join(base_dir, "model-blueprints")
    if os.path.isdir(blueprints_dir):
        for filename in os.listdir(blueprints_dir):
            if not filename.endswith(".md") or filename in ("PROGRESS.md", "INDEX.md"):
                continue
            filepath = os.path.join(blueprints_dir, filename)
            meta, content = parse_frontmatter(filepath)
            if meta and meta.get("id") == item_id:
                return filepath, content

    return None


def cmd_list(args, base_dir):
    """List all items with id, title, score/usage_count only."""
    items = scan_all(base_dir, args.type, args.domain, args.category)

    if not items:
        print("No items found.")
        return

    # Sort: best-practices by score desc, blueprints by usage_count desc
    def sort_key(item):
        meta = item[0]
        return meta.get("score", 0) if item[2] == "best-practice" else meta.get("usage_count", 0) * 10

    items.sort(key=sort_key, reverse=True)

    # Print compact table
    print(f"{'Type':<15} {'Score':<7} {'Uses':<5} {'Domain':<10} {'Category':<14} {'ID':<45} {'Title'}")
    print("-" * 160)

    for meta, filepath, item_type in items:
        score = meta.get("score", "-")
        uses = meta.get("usage_count", 0)
        domain = meta.get("domain", "model") if item_type == "best-practice" else "model"
        category = meta.get("category", "-") if item_type == "best-practice" else "-"
        item_id = meta.get("id", "?")
        title = meta.get("title", "?")

        if item_type == "blueprint":
            score = "-"

        print(
            f"{item_type:<15} "
            f"{str(score):<7} "
            f"{uses:<5} "
            f"{domain:<10} "
            f"{category:<14} "
            f"{item_id:<45} "
            f"{title}"
        )

    print(f"\nTotal: {len(items)} items")


def cmd_get(args, base_dir):
    """Get the full content of one or more items by id."""
    for item_id in args.ids:
        result = find_by_id(base_dir, item_id)
        if result is None:
            print(f"ERROR: Item '{item_id}' not found in any catalog.", file=sys.stderr)
            continue

        filepath, content = result
        print(f"=== {filepath} ===")
        print(content)
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Query best-practices and model-blueprints catalogs"
    )
    parser.add_argument(
        "--base-dir", default=os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()),
        help="Base directory of the project"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # list subcommand
    list_parser = subparsers.add_parser("list", help="List all items (compact: id + title + score)")
    list_parser.add_argument(
        "--type", choices=["best-practice", "bp", "blueprint", "mb", "all"],
        default=None,
        help="Filter by item type"
    )
    list_parser.add_argument(
        "--domain", choices=["model", "backend", "frontend"],
        default=None,
        help="Filter best-practices by domain"
    )
    list_parser.add_argument(
        "--category",
        default=None,
        help="Filter by category (e.g., entity, hook, interceptor)"
    )

    # get subcommand
    get_parser = subparsers.add_parser("get", help="Get full content of item(s) by id")
    get_parser.add_argument("ids", nargs="+", help="One or more item IDs to retrieve")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args, args.base_dir)
    elif args.command == "get":
        cmd_get(args, args.base_dir)


if __name__ == "__main__":
    main()
