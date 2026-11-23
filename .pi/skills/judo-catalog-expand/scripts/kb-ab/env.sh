# Shared settings for the kb A/B harness; override any of these in the environment.
ROOT=$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)
HERE=$ROOT/.pi/skills/judo-catalog-expand/scripts/kb-ab
KBAB_WORK=${KBAB_WORK:-$ROOT/target/kbab}          # plans, run list, metrics, grades
KBAB_TMP=${KBAB_TMP:-/tmp/kbab}                    # one scratch kb project per variant
KBAB_MODEL=${KBAB_MODEL:-anthropic/claude-sonnet-5-5}
KBAB_THINKING=${KBAB_THINKING:-medium}
# kb CLI: the same kb build the pi sessions load (a dev checkout: <pi-agent-dashboard>/packages/kb/bin/kb.mjs)
KB_CLI=${KB_CLI:-$(command -v kb || true)}
# dashboard bus script of the pi-dashboard skill (spawn / until idle / archive)
DASHBOARD_BUS=${DASHBOARD_BUS:-$(find ~/.pi/agent/npm/node_modules "$(npm root -g 2>/dev/null)" -maxdepth 8 -path "*/.pi/skills/pi-dashboard/scripts/dashboard-bus.ts" 2>/dev/null | head -1)}
[ -n "$KB_CLI" ] || { echo "set KB_CLI to the kb CLI (kb.mjs) the sessions use" >&2; exit 1; }
[ -n "$DASHBOARD_BUS" ] || { echo "set DASHBOARD_BUS to pi-dashboard's dashboard-bus.ts" >&2; exit 1; }
kbcli() { case "$KB_CLI" in *.mjs|*.js) node "$KB_CLI" "$@";; *) "$KB_CLI" "$@";; esac; }
# pi names a session folder after the cwd: --<path with / as ->--
sessdir() { local p; p=$(cd "$1" && pwd -P); echo ~/.pi/agent/sessions/--$(echo "${p#/}" | tr / -)--; }
mkdir -p "$KBAB_WORK" "$KBAB_TMP"
