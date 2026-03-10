#!/usr/bin/env bash
#
# Add a new project entry to PROJECTS.md
#
# Usage: add-project.sh <project-name> <git-url> [weight]
#
# The script will:
#   - Clone the repo to get first/last commit info
#   - Add a row to PROJECTS.md
#   - Sort entries by first commit date (newest first = highest priority)
#   - Renumber rows
#
# Examples:
#   add-project.sh "my-project" "git@github.com:org/repo.git"
#   add-project.sh "my-project" "git@github.com:org/repo.git" 5
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECTS_MD="$PROJECT_ROOT/PROJECTS.md"
TEMP_DIR=$(mktemp -d)
CLONE_DIR="$TEMP_DIR/repo"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

cleanup() {
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

usage() {
    echo "Usage: add-project.sh <project-name> <git-url> [weight]"
    echo ""
    echo "Arguments:"
    echo "  project-name  Name of the project (e.g., 'my-awesome-project')"
    echo "  git-url       Git URL (e.g., 'git@github.com:org/repo.git')"
    echo "  weight        Optional weight between -10 and +10 (default: 0)"
    echo ""
    echo "Examples:"
    echo "  add-project.sh 'my-project' 'git@github.com:org/repo.git'"
    echo "  add-project.sh 'my-project' 'git@github.com:org/repo.git' 5"
    exit 1
}

if [[ $# -lt 2 ]]; then
    usage
fi

PROJECT_NAME="$1"
GIT_URL="$2"
WEIGHT="${3:-0}"

# Validate weight
if ! [[ "$WEIGHT" =~ ^-?[0-9]+$ ]] || [[ "$WEIGHT" -lt -10 ]] || [[ "$WEIGHT" -gt 10 ]]; then
    echo -e "${RED}Error: Weight must be an integer between -10 and +10${NC}"
    exit 1
fi

echo -e "${GREEN}Adding project: $PROJECT_NAME${NC}"
echo "Git URL: $GIT_URL"
echo "Weight: $WEIGHT"
echo ""

# Check if project already exists
if grep -q "\\*\\*$PROJECT_NAME\\*\\*" "$PROJECTS_MD"; then
    echo -e "${YELLOW}Warning: Project '$PROJECT_NAME' already exists in PROJECTS.md${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Clone the repo to get commit info
echo -e "${GREEN}Cloning repository to get commit info...${NC}"
if ! git clone --depth 1 "$GIT_URL" "$CLONE_DIR" 2>/dev/null; then
    echo -e "${RED}Error: Failed to clone repository${NC}"
    exit 1
fi

# Get first commit date
FIRST_COMMIT_DATE=$(git -C "$CLONE_DIR" log --reverse --format="%ci" | head -n1 | cut -d' ' -f1)
if [[ -z "$FIRST_COMMIT_DATE" ]]; then
    echo -e "${RED}Error: Could not determine first commit date${NC}"
    exit 1
fi

# Get last commit date
LAST_COMMIT_DATE=$(git -C "$CLONE_DIR" log -1 --format="%ci" | cut -d' ' -f1)

# Get commit count
COMMITS=$(git -C "$CLONE_DIR" rev-list --count HEAD)

echo "First commit: $FIRST_COMMIT_DATE"
echo "Last commit:  $LAST_COMMIT_DATE"
echo "Commits:      $COMMITS"
echo ""

# Create the new row
ROW="|     | **$PROJECT_NAME**       | $GIT_URL | $FIRST_COMMIT_DATE   | $LAST_COMMIT_DATE  | $COMMITS    | $WEIGHT              |"

# Parse PROJECTS.md and build new content
echo -e "${GREEN}Updating PROJECTS.md...${NC}"

HEADER="# JUDO Project Priority Timeline

> Newest projects first (highest priority). Based on first commit date of each repo.
> To add a new project: append one row here. \`/collect-best-practices\` or \`/collect-model-blueprints\` will pick it up automatically.

| #   | Project                    | Git URL                                                       | First Commit | Last Commit | Commits | Weight [-10;+10] |
| --- | -------------------------- | ------------------------------------------------------------- | ------------ | ----------- | ------- | ---------------- |"

# Read existing rows, skip header/separator
ROWS=()
IN_TABLE=false

while IFS= read -r line; do
    if [[ "$line" =~ ^\|[[:space:]]*#[[:space:]]*\| ]]; then
        # Header row
        IN_TABLE=true
        continue
    fi
    if [[ "$line" =~ ^\|[[:space:]]*-+[[:space:]]*\| ]]; then
        # Separator row
        continue
    fi
    if [[ "$line" =~ ^\|[[:space:]]*[0-9]+[[:space:]]*\| ]]; then
        # Data row - extract project name to check for duplicate
        if [[ "$line" =~ \*\*"$PROJECT_NAME"\*\* ]]; then
            echo -e "${YELLOW}Skipping existing entry for $PROJECT_NAME${NC}"
            continue
        fi
        # Convert to pipe-delimited for sorting
        # Extract date (4th column) for sorting
        DATE=$(echo "$line" | cut -d'|' -f5 | xargs)
        ROWS+=("$DATE|$line")
    fi
done < "$PROJECTS_MD"

# Add new row
NEW_ROW_DATE=$FIRST_COMMIT_DATE
ROWS+=("$NEW_ROW_DATE|$ROW")

# Sort by date descending (newest first), then rebuild table
IFS=$'\n' SORTED_ROWS=($(sort -r <<<"${ROWS[*]}"))
unset IFS

# Write output
{
    echo "$HEADER"
    INDEX=1
    for ROW_ENTRY in "${SORTED_ROWS[@]}"; do
        # Remove the date prefix we added for sorting
        ORIGINAL_ROW="${ROW_ENTRY#*|}"
        # Update the row number
        UPDATED_ROW=$(echo "$ORIGINAL_ROW" | sed "s/^[[:space:]]*|[[:space:]]*/| $(printf '%-3s' $INDEX) | /")
        echo "$UPDATED_ROW"
        ((INDEX++))
    done
    echo ""
} > "$PROJECTS_MD.new"

mv "$PROJECTS_MD.new" "$PROJECTS_MD"

echo -e "${GREEN}Done! Added '$PROJECT_NAME' to PROJECTS.md${NC}"
echo ""
echo "Next steps:"
echo "  - Run '/collect-best-practices' or '/collect-model-blueprints' to analyze the new project"
echo "  - Or edit the Weight column in PROJECTS.md to adjust priority"
