- created: 2026-07-12
- created_by: fable-5

## Blockers
- none

## Questions
- ~~(a) drop the Stop hook, or (b) architect as orchestrator-dispatched subagent?~~
  RULED (operator, 2026-07-20): neither as posed — **the finishing hooks are replaced by
  MESSAGE BUS choreography.** The close handshake (THAT IS ALL / ALL IT IS → return
  focus, cleanup) and end-of-session signalling ride the repo bus, not
  transcript-grepping Stop hooks. Include the bus fixes needed for reliable usage
  (the liveness gap: announce proves load, nothing catches a mid-session death —
  [[bus-liveness]]; metadata on the bus — [[agent-metadata]]).

## Findings
- architect-close.sh greps transcripts with jq, juggles tmux sockets, fails silently;
  the operator distrusts it. Worktree sessions also ran with broken relative skill
  symlinks pre-orchids (absolute links fixed that) — part of the past pain.
- 2026-07-20 close-miss diagnosed (role-dag-frontmatter close): the hook's
  `jq -s` slurp dies on a partial trailing transcript line — the Stop hook races
  the harness's final append (transcript mtime 19:38:25 vs hook fire 19:37:33) —
  so extraction collapses to `''` and the countersign never matches. Reproduced
  by truncating the transcript tail. A per-line `jq -R 'fromjson?'` parse over
  the same truncated file still extracts `ALL IT IS`; operator ruled to leave the hook
  broken and replace the mechanism (this task).
- The shared settings.json Stop entry fires the hook in EVERY session on the
  box, and on no-match it logs that session's last-message tail to
  /tmp/architect-close.log — cross-session conversation content leaks into a
  /tmp file. The replacement kills this leak.
- [[tmux-topology]] reshapes the same choreography (window-per-architect, focus
  return on close) — co-design so the bus signals drive whatever layout is current.

## Proposal
Close and finishing choreography over the message bus: the architect signals its
lifecycle on the bus; the orchestrator (or its bus sidecar) acts on those signals —
focus return, pane/window cleanup, close dispatch — with no transcript parsing
anywhere. Fix the bus reliability gaps this depends on. HOW — signal set, who
listens, hook retirement order — is the architect's tech plan (Decision-025/027).

## Testing
One full feature cycle (spawn → MAKE IT SO → THAT IS ALL/ALL IT IS → close) driven
end-to-end by bus messages: focus returns, the architect's pane closes, no
architect-close.sh in the path, and /tmp/architect-close.log records nothing. A
deliberately killed architect is detected rather than silently absent.
