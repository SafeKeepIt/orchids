- created: 2026-07-12
- created_by: fable-5

## Blockers
- none

## Questions
- (a) drop the Stop hook (operator returns via orch; ALL IT IS stays a text marker),
  (b) architect as orchestrator-dispatched subagent — but subagents cannot talk to
  the operator mid-flight, and the MAKE IT SO gate is interactive (why Opus called
  agents the wrong tool). Which trade does the operator want?

## Findings
- architect-close.sh greps transcripts with jq, juggles tmux sockets, fails silently;
  the operator distrusts it. Worktree sessions also ran with broken relative skill
  symlinks pre-orchids (absolute links fixed that) — part of the past pain.

## Proposal
Prototype (a) first — cheapest; revisit (b) when background-agent messaging allows
operator interaction.

## Testing
One full feature cycle (spawn → MAKE IT SO → THAT IS ALL/ALL IT IS → close) without
the hook, measuring operator friction.
