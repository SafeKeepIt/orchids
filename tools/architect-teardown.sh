#!/usr/bin/env bash
# Message-bus choreography teardown action.
# Called by the ORCHESTRATOR on the architect's `finished` signal to return the
# operator's tmux client to the orchestrator pane and close the architect's pane.
# Replaces the retired Stop hook — no transcript reading, no stdin, no scratch-file logging.
# Best-effort: every tmux call is guarded, always exit 0.
set -u

if [ -z "${1:-}" ]; then
  echo "usage: architect-teardown.sh <feature-id>" >&2
  exit 0
fi

id="$1"
wt=".claude/worktrees/$id"
rw="$wt/.return-window"

if [ ! -f "$rw" ]; then
  echo "architect-teardown: no .return-window for $id"
  exit 0
fi

ret=$(sed -n 1p "$rw")
sock=$(sed -n 2p "$rw")
[ -n "$sock" ] || sock="${TMUX%%,*}"
if [ -z "$sock" ]; then
  echo "architect-teardown: no tmux socket available for $id"
  exit 0
fi

tx(){ tmux -S "$sock" "$@" 2>/dev/null || true; }

# architect pane is found by TITLE — the orchestrator has no $TMUX_PANE for it
arch=$(tx list-panes -a -F '#{pane_id} #{pane_title}' | awk -v t="arch:$id" '$2==t{print $1; exit}')

# focus return — line 1 is a pane id %N (Decision-006) or legacy window id @N
case "$ret" in
  %*) ret_win=$(tx display-message -p -t "$ret" '#{window_id}'); tx switch-client -t "$ret"; [ -n "$ret_win" ] && tx select-window -t "$ret_win"; tx select-pane -t "$ret" ;;
  *)  ret_win="$ret"; tx switch-client -t "$ret" || tx select-window -t "$ret" ;;
esac

arch_win=""
[ -n "$arch" ] && arch_win=$(tx display-message -p -t "$arch" '#{window_id}')

# SAFETY: never kill the return target or its window
if [ -z "$arch" ]; then
  echo "architect-teardown: no architect pane found for $id, not closing"
  exit 0
fi
if [ "$arch" = "$ret" ]; then
  echo "architect-teardown: architect pane equals return target, not closing"
  exit 0
fi
if [ -n "$ret_win" ] && [ "$arch_win" = "$ret_win" ]; then
  echo "architect-teardown: architect pane shares window with return target, not closing"
  exit 0
fi

tx kill-pane -t "$arch"
echo "architect-teardown: returned to $ret, closed $arch"
exit 0
