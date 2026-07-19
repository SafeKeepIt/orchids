#!/usr/bin/env bash
# SessionEnd hook — take this session off the message bus.
#
# Two signals, deliberately at different layers:
#   1. a departure broadcast, so live agents learn of it inside the agentic flow;
#   2. removal of the inbox, which is the structural signal — a later send to this
#      session then fails immediately instead of writing into a folder nobody is
#      watching. That failure is the whole reason the folder is torn down.
#
# Undelivered messages die with the inbox. That is correct, not a leak: the bus
# offers NO delivery guarantee, and a sender is expected to decide for itself
# whether to retry, abandon, or error.
set -eu

root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
for candidate in "$root/.claude/tools/bus.py" "$root/tools/bus.py"; do
  [ -f "$candidate" ] && bus="$candidate" && break
done
[ -n "${bus:-}" ] || exit 0

python3 "$bus" depart   >/dev/null 2>&1 || true
python3 "$bus" teardown >/dev/null 2>&1 || true
exit 0
