#!/usr/bin/env bash
# SessionStart hook — give every session in this repository a mailbox.
#
# Two jobs, and only the first is enforceable from a shell:
#   1. create this agent's inbox (structural — it exists whatever the model does);
#   2. inject the instruction to load the bus sidecar (a model action; a hook cannot
#      spawn a subagent, so this step is prompted, not enforced).
#
# The injection deliberately carries NO identity and NO path. An agent that skips
# loading its bus therefore cannot address anything, cannot be addressed, and does
# not know its own name — the gate is the capability itself rather than a nudge.
set -eu

root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
# consuming repos get it laid at .claude/tools/; orchids itself holds the source
for candidate in "$root/.claude/tools/bus.py" "$root/tools/bus.py"; do
  [ -f "$candidate" ] && bus="$candidate" && break
done
[ -n "${bus:-}" ] || exit 0

# Structural half: the inbox exists even if the model ignores everything below.
python3 "$bus" init >/dev/null 2>&1 || exit 0

cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"MESSAGING: you can exchange messages with the other agents in this repository. Load your bus sidecar now — spawn a subagent with subagent_type \"bus\" and the prompt \"You are my bus. Report my identity and how to reach the others.\" It is your ONLY means of sending or receiving, and it will tell you who you are. Do this before starting work: messages addressed to you are already accumulating, and without a bus you will never see them."}}
JSON
