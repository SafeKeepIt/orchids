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
- 2026-07-20 close-miss diagnosed (role-dag-frontmatter close): the hook's
  `jq -s` slurp dies on a partial trailing transcript line — the Stop hook races
  the harness's final append (transcript mtime 19:38:25 vs hook fire 19:37:33) —
  so extraction collapses to `''` and the countersign never matches. Reproduced
  by truncating the transcript tail. A per-line `jq -R 'fromjson?'` parse over
  the same truncated file still extracts `ALL IT IS`; that is the tactical fix.
- The shared settings.json Stop entry fires the hook in EVERY session on the
  box, and on no-match it logs that session's last-message tail to
  /tmp/architect-close.log — cross-session conversation content leaks into a
  /tmp file. Fold into whichever choreography replaces the hook.

## Proposal
Prototype (a) first — cheapest; revisit (b) when background-agent messaging allows
operator interaction.

## Testing
One full feature cycle (spawn → MAKE IT SO → THAT IS ALL/ALL IT IS → close) without
the hook, measuring operator friction.
