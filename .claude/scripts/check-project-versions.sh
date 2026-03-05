#!/usr/bin/env bash
# check-project-versions.sh
# Reads PROJECTS.md and blueprint/PROGRESS.md, compares remote HEAD SHA
# vs last-analyzed SHA, outputs a comparison table.
#
# Usage: bash .claude/scripts/check-project-versions.sh [PROJECTS.md path] [PROGRESS.md path]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

PROJECTS_FILE="${1:-$PROJECT_ROOT/PROJECTS.md}"
PROGRESS_FILE="${2:-$PROJECT_ROOT/blueprint/PROGRESS.md}"

if [[ ! -f "$PROJECTS_FILE" ]]; then
    echo "ERROR: PROJECTS.md not found at $PROJECTS_FILE" >&2
    exit 1
fi

# Parse PROGRESS.md for last-analyzed SHAs (project -> SHA mapping)
declare -A LAST_SHA
if [[ -f "$PROGRESS_FILE" ]]; then
    while IFS='|' read -r _ _ project _ _ _ sha _ _; do
        project=$(echo "$project" | xargs)
        sha=$(echo "$sha" | xargs)
        if [[ -n "$project" && "$project" != "Project" && "$project" != "---" ]]; then
            LAST_SHA["$project"]="$sha"
        fi
    done < "$PROGRESS_FILE"
fi

# Header
printf "%-30s %-12s %-12s %s\n" "Project" "Remote SHA" "Last SHA" "Status"
printf "%-30s %-12s %-12s %s\n" "-------" "----------" "--------" "------"

# Counters
CHANGED=0
UNCHANGED=0
NEW=0
ERRORS=0

# Parse PROJECTS.md table rows and check each project
while IFS='|' read -r _ num project url first_commit last_commit commits _; do
    # Skip header, separator, and empty rows
    project=$(echo "$project" | xargs | sed 's/\*\*//g')
    url=$(echo "$url" | xargs)

    [[ -z "$project" || "$project" == "Project" || "$project" == "---" ]] && continue
    [[ -z "$url" || "$url" == "Git URL" ]] && continue

    # Get remote HEAD SHA
    remote_sha=$(git ls-remote "$url" HEAD 2>/dev/null | cut -c1-7) || remote_sha="ERROR"

    if [[ "$remote_sha" == "ERROR" || -z "$remote_sha" ]]; then
        printf "%-30s %-12s %-12s %s\n" "$project" "ERROR" "-" "ERROR"
        ((ERRORS++))
        continue
    fi

    # Get last analyzed SHA from PROGRESS.md
    last_sha="${LAST_SHA[$project]:-}"

    if [[ -z "$last_sha" || "$last_sha" == "-" ]]; then
        printf "%-30s %-12s %-12s %s\n" "$project" "$remote_sha" "-" "NEW"
        ((NEW++))
    elif [[ "$remote_sha" == "$last_sha" ]]; then
        printf "%-30s %-12s %-12s %s\n" "$project" "$remote_sha" "$last_sha" "unchanged"
        ((UNCHANGED++))
    else
        printf "%-30s %-12s %-12s %s\n" "$project" "$remote_sha" "$last_sha" "CHANGED"
        ((CHANGED++))
    fi
done < "$PROJECTS_FILE"

echo ""
echo "Summary: $CHANGED changed, $NEW new, $UNCHANGED unchanged, $ERRORS errors"
