#!/usr/bin/env bash
# Validate blueprint mutations against a Sandbox model using judo-cli.
#
# Uses **direct TCP** to the CLI server for speed: the first call spawns
# a JVM server (~2s), then all mutations go over a plain TCP socket (~10ms each).
#
# For each blueprint .md file:
#   1. Extracts all GraphQL mutation code blocks
#   2. Substitutes {{PLACEHOLDER}} tokens with Sandbox-compatible values
#   3. Runs each mutation via direct TCP to the CLI server
#   4. Sends discard --force via TCP to reset the model
#   5. Reports pass/fail per blueprint
#
# The CLI server auto-starts on first call and auto-stops after idle timeout.
# We never manually stop it.
#
# Exit code 0 = all pass, 1 = at least one failure, 2 = setup error.
#
# Usage:
#   tests/test-blueprint-mutations.sh                      # test all
#   tests/test-blueprint-mutations.sh --blueprint <id>     # test one
set -euo pipefail

# ---- Configuration ----
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BLUEPRINTS_DIR="$PROJECT_ROOT/model-blueprints"
SANDBOX_MODEL="$SCRIPT_DIR/fixtures/Sandbox.model"

DEFAULT_CLI="$PROJECT_ROOT/.claude/judo-cli.jar"
JUDO_CLI_JAR="${JUDO_CLI_JAR:-$DEFAULT_CLI}"

CLI_TIMEOUT=60

# Server port (discovered after warm-up)
SERVER_PORT=""

# ---- Counters ----
TOTAL_BP=0
PASSED_BP=0
FAILED_BP=0
SKIPPED_BP=0
AUTO_COUNTER=0

# ---- Server discovery ----

discover_server_port() {
    local model_abs
    model_abs="$(realpath "$SANDBOX_MODEL")"

    for f in "$HOME/.judo/sessions"/*/session.json; do
        [[ -f "$f" ]] || continue
        if grep -q "\"$model_abs\"" "$f" 2>/dev/null; then
            local port
            port="$(grep '"port"' "$f" | grep -o '[0-9]\+')"
            if [[ -n "$port" ]] && (echo "" > /dev/tcp/localhost/"$port") 2>/dev/null; then
                SERVER_PORT="$port"
                return 0
            fi
        fi
    done
    return 1
}

warm_up_server() {
    echo "Starting CLI server (one-time JVM startup)..."
    timeout "$CLI_TIMEOUT" java -jar "$JUDO_CLI_JAR" -m "$SANDBOX_MODEL" -q graphql \
        '{ esm { count(type: "EntityType") } }' >/dev/null 2>&1

    if ! discover_server_port; then
        echo "ERROR: Could not discover server port after warm-up" >&2
        return 1
    fi
    echo "Server ready on port $SERVER_PORT (direct TCP mode)"
}

# ---- Direct TCP communication ----

send_command() {
    local cmd_line="EXEC -q"
    for arg in "$@"; do
        local escaped="${arg//$'\n'/ }"
        escaped="${escaped//\"/\\\"}"
        if [[ "$escaped" == *" "* || "$escaped" == *"'"* ]]; then
            cmd_line="$cmd_line \"$escaped\""
        else
            cmd_line="$cmd_line $escaped"
        fi
    done

    exec 3<>/dev/tcp/localhost/"$SERVER_PORT"
    echo "$cmd_line" >&3

    local output=""
    local exit_code=0
    while IFS= read -r line <&3; do
        if [[ "$line" == "END" ]]; then
            break
        elif [[ "$line" == EXIT:* ]]; then
            exit_code="${line#EXIT:}"
        else
            output="${output}${line}"$'\n'
        fi
    done
    exec 3>&-

    echo "$output"
    return "$exit_code"
}

# ---- Placeholder substitution ----
substitute_placeholders() {
    local mutation="$1"
    mutation="${mutation//\{\{TYPES_NAMESPACE\}\}/Sandbox::types}"
    mutation="${mutation//\{\{MEASURES_NAMESPACE\}\}/Sandbox::measures}"
    mutation="${mutation//\{\{NAMESPACE\}\}/Sandbox}"

    while [[ "$mutation" =~ \{\{([A-Z_0-9]+)\}\} ]]; do
        local token="${BASH_REMATCH[1]}"
        local tag="{{${token}}}"
        local replacement
        if [[ "$token" == *ORDINAL* || "$token" == *COUNT* || "$token" == *BOUND* ]]; then
            AUTO_COUNTER=$((AUTO_COUNTER + 1))
            replacement="$AUTO_COUNTER"
        elif [[ "$token" == *FQN* || "$token" == *NAMESPACE* ]]; then
            replacement="Sandbox"
        else
            local lower="${token,,}"
            lower="${lower//_/}"
            replacement="Test${lower^}"
            replacement="${replacement:0:24}"
        fi
        mutation="${mutation//$tag/$replacement}"
    done
    echo "$mutation"
}

# ---- Test a single blueprint ----
test_blueprint() {
    local md_path="$1"
    local blueprint_id
    blueprint_id="$(basename "$md_path" .md)"
    AUTO_COUNTER=0

    local mutations=()
    while IFS= read -r -d $'\x00' m; do
        mutations+=("$m")
    done < <(awk '
        /^```graphql/ { in_block=1; block=""; next }
        /^```/ && in_block {
            in_block=0
            if (block ~ /^mutation/) { printf "%s\0", block }
            next
        }
        in_block { block = block (block ? "\n" : "") $0 }
    ' "$md_path")

    local total=${#mutations[@]}

    if [[ $total -eq 0 ]]; then
        printf "%-55s SKIP (no mutations)\n" "$blueprint_id"
        SKIPPED_BP=$((SKIPPED_BP + 1))
        return 0
    fi

    local passed=0
    local failed=0
    local failures=""

    for i in "${!mutations[@]}"; do
        local idx=$((i + 1))
        local raw="${mutations[$i]}"
        local substituted
        substituted="$(substitute_placeholders "$raw")"

        local output
        output="$(send_command graphql "$substituted")" || true

        if echo "$output" | grep -q '"success" : true\|"success":true'; then
            passed=$((passed + 1))
        else
            failed=$((failed + 1))
            local err_msg=""
            if echo "$output" | grep -q '"message"'; then
                err_msg="$(echo "$output" | grep -o '"message" *: *"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')"
            fi
            [[ -z "$err_msg" ]] && err_msg="unknown error"
            failures="${failures}\n  #${idx}: ${err_msg:0:120}"
        fi
    done

    # Discard to reset model for next blueprint
    send_command discard --force >/dev/null 2>&1 || true

    if [[ $failed -eq 0 ]]; then
        printf "%-55s PASS (%d/%d)\n" "$blueprint_id" "$passed" "$total"
        PASSED_BP=$((PASSED_BP + 1))
    else
        printf "%-55s FAIL (%d/%d)\n" "$blueprint_id" "$passed" "$total"
        printf "%b\n" "$failures"
        FAILED_BP=$((FAILED_BP + 1))
    fi
}

# ---- Main ----

SINGLE_BLUEPRINT=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --blueprint) SINGLE_BLUEPRINT="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 2 ;;
    esac
done

if [[ ! -f "$JUDO_CLI_JAR" ]]; then
    echo "ERROR: judo-cli.jar not found at $JUDO_CLI_JAR" >&2
    echo "Set JUDO_CLI_JAR env var or run: mvn validate -P download-model-cli" >&2
    exit 2
fi

if [[ ! -f "$SANDBOX_MODEL" ]]; then
    echo "ERROR: Sandbox model not found at $SANDBOX_MODEL" >&2
    exit 2
fi

if [[ -n "$SINGLE_BLUEPRINT" ]]; then
    md="$BLUEPRINTS_DIR/${SINGLE_BLUEPRINT}.md"
    if [[ ! -f "$md" ]]; then
        echo "ERROR: Blueprint not found: $md" >&2
        exit 2
    fi
    files=("$md")
else
    files=()
    for f in "$BLUEPRINTS_DIR"/*.md; do
        local_name="$(basename "$f")"
        [[ "$local_name" == "PROGRESS.md" || "$local_name" == "CONVENTIONS.md" ]] && continue
        files+=("$f")
    done
fi

if [[ ${#files[@]} -eq 0 ]]; then
    echo "No blueprint files found." >&2
    exit 2
fi

if ! warm_up_server; then
    echo "ERROR: Failed to start CLI server" >&2
    exit 2
fi

START_TIME=$SECONDS

for md_path in "${files[@]}"; do
    TOTAL_BP=$((TOTAL_BP + 1))
    test_blueprint "$md_path"
done

ELAPSED=$((SECONDS - START_TIME))

echo ""
echo "============================================================"
echo "SUMMARY: $TOTAL_BP blueprints | $PASSED_BP PASS | $FAILED_BP FAIL | $SKIPPED_BP SKIP"
echo "Elapsed: ${ELAPSED}s"
echo "============================================================"

if [[ $FAILED_BP -gt 0 ]]; then
    exit 1
fi
exit 0
