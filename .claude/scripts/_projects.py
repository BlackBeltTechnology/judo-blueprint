"""
Shared helper to parse PROJECTS.md into project order and weight data.

Used by both score-best-practices.py and score-model-blueprints.py.
"""

import os
import re


def parse_projects_md(base_dir):
    """Parse PROJECTS.md table and return project order + weights.

    Returns:
        project_order: dict mapping project_name -> recency index
                       (higher index = newer project = more recency bonus)
        project_weights: dict mapping project_name -> weight (int)
        total_projects: total number of projects in the table
    """
    projects_path = os.path.join(base_dir, "PROJECTS.md")
    if not os.path.isfile(projects_path):
        return {}, {}, 0

    with open(projects_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse markdown table rows (skip header and separator)
    rows = []
    in_table = False
    for line in content.split("\n"):
        line = line.strip()
        if not line.startswith("|"):
            in_table = False
            continue
        if not in_table:
            # First row is header
            in_table = True
            continue
        if re.match(r"^\|\s*-", line):
            # Separator row
            continue
        rows.append(line)

    # Each row: | # | **name** | git_url | first_commit | last_commit | commits | weight |
    project_order = {}
    project_weights = {}
    total = len(rows)

    for row in rows:
        cells = [c.strip() for c in row.split("|")]
        # Split by | gives empty first/last elements
        cells = [c for c in cells if c != ""]
        if len(cells) < 2:
            continue

        row_num = cells[0].strip()
        if not re.match(r"^\d+$", row_num):
            continue
        row_num = int(row_num)

        # Extract project name from **name** format
        name_match = re.search(r"\*\*(.+?)\*\*", cells[1])
        if not name_match:
            continue
        project_name = name_match.group(1)

        # Recency index: newest (#1) gets highest index
        project_order[project_name] = total - row_num + 1

        # Weight column (last column, optional)
        weight = 0
        if len(cells) >= 7:
            weight_str = cells[6].strip()
            weight_match = re.match(r"^[+-]?\d+$", weight_str)
            if weight_match:
                weight = int(weight_str)
        project_weights[project_name] = weight

    return project_order, project_weights, total
