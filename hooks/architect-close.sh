#!/usr/bin/env bash
# Stop hook. When the architect countersigns the operator's "THAT IS ALL" with a final
# "ALL IT IS", return the tmux client to the orchestrator window (captured at spawn in
# .return-window) and close the architect's OWN window. No-op for any other agent/message.
# Logs every invocation to /tmp/architect-close.log so a miss is diagnosable.
set -eu

log=/tmp/architect-close.log
ts=$(date '+%F %T' 2>/dev/null || echo '?')
say(){ printf '%s [close-hook] %s\n' "$ts" "$1" >> "$log" 2>/dev/null || true; }

input=$(cat)
tp=$(printf '%s' "$input" | jq -r '.transcript_path // empty' 2>/dev/null || true)
root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")
rw="$root/.return-window"

[ -n "$tp" ] && [ -f "$tp" ] || { say "no transcript (tp='$tp')"; exit 0; }

last=$(jq -rs 'map(select(.type=="assistant")) | last // {} | (.message.content // []) | map(select(.type=="text").text) | join("")' "$tp" 2>/dev/null || true)
last=$(printf '%s' "$last" | sed -e 's/[[:space:]]*$//' | awk 'NF{l=$0} END{print l}')
[ "$last" = "ALL IT IS" ] || { say "no match (last='$last')"; exit 0; }
[ -f "$rw" ] || { say "match but no .return-window at $rw"; exit 0; }

orch=$(sed -n 1p "$rw" 2>/dev/null || true)
sock=$(sed -n 2p "$rw" 2>/dev/null || true)
[ -n "$sock" ] || sock="${TMUX%%,*}"        # fall back to inherited $TMUX socket
tx(){ tmux -S "$sock" "$@"; }

# the architect's OWN window, via the pane this hook runs in (NOT the "current" window,
# which may be elsewhere if the operator switched away)
arch=$(tx display-message -p -t "${TMUX_PANE:-}" '#{window_id}' 2>/dev/null || true)
say "MATCH orch='$orch' sock='$sock' pane='${TMUX_PANE:-}' arch='$arch'"

[ -n "$sock" ] || { say "no tmux socket — leaving window for manual close"; exit 0; }
# SAFETY: never kill the orchestrator window. If our pane resolved to it (mis-fire,
# e.g. focus elsewhere), return only and leave the window alone.
if [ -z "$arch" ] || [ "$arch" = "$orch" ]; then
  say "arch='$arch' == orch or empty — returning only, NOT killing"
  tx switch-client -t "$orch" 2>/dev/null || tx select-window -t "$orch" 2>/dev/null || say "return to $orch FAILED"
  exit 0
fi
tx switch-client -t "$orch" 2>/dev/null || tx select-window -t "$orch" 2>/dev/null || say "return to $orch FAILED"
tx kill-window -t "$arch" 2>/dev/null || say "kill $arch FAILED"
exit 0
