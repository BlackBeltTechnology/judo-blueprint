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
  python3 query-catalog.py list --type blueprint --layer backend  # Blueprints that have backend.md
  python3 query-catalog.py list --domain model                # Only model-domain best-practices
  python3 query-catalog.py list --domain model --type all     # Model best-practices + blueprints
  python3 query-catalog.py list --category entity             # Filter by category
  python3 query-catalog.py list --project mlszksz-platform    # Items that reference a project
  python3 query-catalog.py list --where usage_count=3         # Generic frontmatter filter
  python3 query-catalog.py list --where score=68.0 --type blueprint  # Combine filters
  python3 query-catalog.py get audit-log-entity               # Full content (BLUEPRINT.md + model.md)
  python3 query-catalog.py get audit-log-entity --layer backend   # Only backend.md content
  python3 query-catalog.py get audit-log-entity --layer frontend  # Only frontend.md content
  python3 query-catalog.py get audit-log-entity --layer model     # Only model.md content
  python3 query-catalog.py get audit-log-entity --layer all       # All files concatenated
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


def detect_blueprint_layers(blueprint_dir):
    """Detect which layer files exist in a blueprint directory."""
    layers = []
    for layer in ["model", "backend", "frontend"]:
        if os.path.isfile(os.path.join(blueprint_dir, f"{layer}.md")):
            layers.append(layer)
    return layers


def match_where(meta, where_filters):
    """Check if a meta dict matches all --where KEY=VALUE filters.

    Supports:
      - Scalar match: key=value (string, int, or float comparison)
      - List membership: if the frontmatter value is a list, checks if value is in it
      - Numeric comparisons: key>N, key>=N, key<N, key<=N
    """
    for expr in where_filters:
        for op in (">=", "<=", ">", "<", "="):
            if op in expr:
                key, val = expr.split(op, 1)
                key = key.strip()
                val = val.strip()
                break
        else:
            continue

        meta_val = meta.get(key)
        if meta_val is None:
            return False

        if op == "=":
            if isinstance(meta_val, list):
                if val not in meta_val:
                    return False
            elif isinstance(meta_val, (int, float)):
                try:
                    if meta_val != type(meta_val)(val):
                        return False
                except (ValueError, TypeError):
                    if str(meta_val) != val:
                        return False
            else:
                if str(meta_val) != val:
                    return False
        else:
            # Numeric comparison
            try:
                num_meta = float(meta_val) if not isinstance(meta_val, (int, float)) else meta_val
                num_val = float(val)
            except (ValueError, TypeError):
                return False
            if op == ">" and not (num_meta > num_val):
                return False
            elif op == ">=" and not (num_meta >= num_val):
                return False
            elif op == "<" and not (num_meta < num_val):
                return False
            elif op == "<=" and not (num_meta <= num_val):
                return False

    return True


def scan_all(base_dir, type_filter=None, domain_filter=None, category_filter=None,
             layer_filter=None, project_filter=None, where_filters=None):
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

    # Scan model-blueprints (directory-based: model-blueprints/<id>/BLUEPRINT.md)
    if type_filter in (None, "all", "blueprint", "mb"):
        blueprints_dir = os.path.join(base_dir, "model-blueprints")
        if os.path.isdir(blueprints_dir):
            for entry in sorted(os.listdir(blueprints_dir)):
                subdir = os.path.join(blueprints_dir, entry)
                if not os.path.isdir(subdir):
                    continue
                bp_file = os.path.join(subdir, "BLUEPRINT.md")
                if os.path.isfile(bp_file):
                    meta, _ = parse_frontmatter(bp_file)
                    if meta:
                        layers = detect_blueprint_layers(subdir)
                        meta["_layers"] = layers
                        # Apply layer filter: only include blueprints that have the requested layer
                        if layer_filter and layer_filter != "all":
                            if layer_filter not in layers:
                                continue
                        items.append((meta, bp_file, "blueprint"))

    # Apply category filter
    if category_filter:
        items = [(m, f, t) for m, f, t in items if m.get("category", "") == category_filter]

    # Apply project filter (check if project is in the projects list)
    if project_filter:
        items = [(m, f, t) for m, f, t in items
                 if project_filter in m.get("projects", [])]

    # Apply generic --where filters
    if where_filters:
        items = [(m, f, t) for m, f, t in items if match_where(m, where_filters)]

    return items


def find_by_id(base_dir, item_id, layer=None):
    """Find a specific item by its id across all catalogs.

    For blueprints, the layer parameter controls what content is returned:
      None or "all"  -> BLUEPRINT.md + model.md (default, backward compatible)
      "model"        -> only model.md
      "backend"      -> only backend.md
      "frontend"     -> only frontend.md

    Returns (filepath, full_content) or None.
    """
    # Check best-practices (all domains) — layer filter doesn't apply here
    if layer in (None, "all"):
        for domain in ["model", "backend", "frontend"]:
            filepath = os.path.join(base_dir, "best-practices", domain, f"{item_id}.md")
            if os.path.isfile(filepath):
                meta, content = parse_frontmatter(filepath)
                if meta and meta.get("id") == item_id:
                    return filepath, content

    # Check model-blueprints (directory-based)
    bp_dir = os.path.join(base_dir, "model-blueprints", item_id)
    bp_file = os.path.join(bp_dir, "BLUEPRINT.md")
    if os.path.isfile(bp_file):
        meta, content = parse_frontmatter(bp_file)
        if meta and meta.get("id") == item_id:
            # Return specific layer file
            if layer and layer != "all":
                layer_file = os.path.join(bp_dir, f"{layer}.md")
                if os.path.isfile(layer_file):
                    with open(layer_file, "r", encoding="utf-8") as f:
                        return layer_file, f.read()
                else:
                    return None  # requested layer doesn't exist
            # Default: BLUEPRINT.md + model.md concatenated
            model_file = os.path.join(bp_dir, "model.md")
            if os.path.isfile(model_file):
                with open(model_file, "r", encoding="utf-8") as f:
                    content += "\n" + f.read()
            # If --layer all, also append backend.md and frontend.md
            if layer == "all":
                for extra in ["backend.md", "frontend.md"]:
                    extra_file = os.path.join(bp_dir, extra)
                    if os.path.isfile(extra_file):
                        with open(extra_file, "r", encoding="utf-8") as f:
                            content += "\n" + f.read()
            return bp_file, content

    # Fallback: scan all best-practice files in case filename != id
    if layer in (None, "all"):
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

    # Fallback: scan blueprint directories
    blueprints_dir = os.path.join(base_dir, "model-blueprints")
    if os.path.isdir(blueprints_dir):
        for entry in os.listdir(blueprints_dir):
            subdir = os.path.join(blueprints_dir, entry)
            if not os.path.isdir(subdir):
                continue
            bp_file = os.path.join(subdir, "BLUEPRINT.md")
            if os.path.isfile(bp_file):
                meta, content = parse_frontmatter(bp_file)
                if meta and meta.get("id") == item_id:
                    if layer and layer != "all":
                        layer_file = os.path.join(subdir, f"{layer}.md")
                        if os.path.isfile(layer_file):
                            with open(layer_file, "r", encoding="utf-8") as f:
                                return layer_file, f.read()
                        else:
                            return None
                    model_file = os.path.join(subdir, "model.md")
                    if os.path.isfile(model_file):
                        with open(model_file, "r", encoding="utf-8") as f:
                            content += "\n" + f.read()
                    if layer == "all":
                        for extra in ["backend.md", "frontend.md"]:
                            extra_file = os.path.join(subdir, extra)
                            if os.path.isfile(extra_file):
                                with open(extra_file, "r", encoding="utf-8") as f:
                                    content += "\n" + f.read()
                    return bp_file, content

    return None


def cmd_list(args, base_dir):
    """List all items with id, title, score/usage_count only."""
    items = scan_all(base_dir, args.type, args.domain, args.category, args.layer,
                     args.project, args.where)

    if not items:
        print("No items found.")
        return

    # Sort: best-practices by score desc, blueprints by usage_count desc
    def sort_key(item):
        meta = item[0]
        return meta.get("score", 0) if item[2] == "best-practice" else meta.get("usage_count", 0) * 10

    items.sort(key=sort_key, reverse=True)

    # Print compact table
    print(f"{'Type':<15} {'Score':<7} {'Uses':<5} {'Domain':<10} {'Layers':<14} {'ID':<45} {'Title'}")
    print("-" * 160)

    for meta, filepath, item_type in items:
        score = meta.get("score", "-")
        uses = meta.get("usage_count", 0)
        domain = meta.get("domain", "model") if item_type == "best-practice" else "model"
        item_id = meta.get("id", "?")
        title = meta.get("title", "?")

        if item_type == "blueprint":
            score = "-"
            layers = ",".join(meta.get("_layers", []))
        else:
            category = meta.get("category", "-")
            layers = category

        print(
            f"{item_type:<15} "
            f"{str(score):<7} "
            f"{uses:<5} "
            f"{domain:<10} "
            f"{layers:<14} "
            f"{item_id:<45} "
            f"{title}"
        )

    print(f"\nTotal: {len(items)} items")


def cmd_get(args, base_dir):
    """Get the full content of one or more items by id."""
    layer = getattr(args, "layer", None)
    for item_id in args.ids:
        result = find_by_id(base_dir, item_id, layer=layer)
        if result is None:
            if layer:
                print(f"ERROR: Item '{item_id}' not found or has no {layer}.md layer.", file=sys.stderr)
            else:
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
    list_parser.add_argument(
        "--layer", choices=["model", "backend", "frontend", "all"],
        default=None,
        help="Filter blueprints by which layer files exist (model, backend, frontend)"
    )
    list_parser.add_argument(
        "--project",
        default=None,
        help="Filter items that reference this project in their projects list"
    )
    list_parser.add_argument(
        "--where", nargs="+", metavar="KEY=VALUE",
        default=None,
        help="Generic frontmatter filter(s). Supports =, >, >=, <, <= (e.g., usage_count>=3, score>40)"
    )

    # get subcommand
    get_parser = subparsers.add_parser("get", help="Get full content of item(s) by id")
    get_parser.add_argument("ids", nargs="+", help="One or more item IDs to retrieve")
    get_parser.add_argument(
        "--layer", choices=["model", "backend", "frontend", "all"],
        default=None,
        help="Return only a specific layer file (model.md, backend.md, frontend.md) or all files"
    )

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args, args.base_dir)
    elif args.command == "get":
        cmd_get(args, args.base_dir)


if __name__ == "__main__":
    main()
