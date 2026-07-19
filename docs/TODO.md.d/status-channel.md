- created: 2026-07-19
- created_by: fable-5
- created_during: f/status-channel

## Blockers

_None._

## Questions

- Can the operator's pane suppress per-event Monitor lines? The operator believes it is
  optional; the `Monitor` tool schema exposes no display control and no config tool is
  reachable from a session. Does not block the feature — only how noisy it looks.

## Findings

Established empirically 2026-07-19 (each verified, not inferred):

- **`SendMessage` reaches only agents spawned from within your own session.** A separate
  process with a name and a registry id is NOT reachable — tested against a purpose-built
  background session and against a foreign one, by name, by short id and by sessionId, all
  rejected. Discoverability is not addressability.
- **A subagent CAN push to its parent unprompted.** `SendMessage(to: "main")` from a subagent
  that was never messaged first returns `"Message queued for the main conversation's next
  turn."` and arrives wrapped as `<agent-message from=…>` with a harness warning that it is
  not user input — so an agent message structurally cannot impersonate operator authority.
- **An event creates a turn.** Notifications wake an otherwise-idle session; no polling loop
  is needed, and an idle or finished subagent costs nothing while waiting.
- **Monitor events land with whoever ARMED the monitor.** A subagent-armed monitor delivered
  all events to the subagent; the parent received none (verified by token absence). This is
  what keeps the raw stream out of the orchestrator's context.
- **The operator sees only the monitor's `description`, once per event — never the payload.**
  So `description` is operator-facing copy, not a debug label, and the payload is invisible
  to them (which is why a rendered board is the only informative artefact).
- **No CLI route injects a turn into a live session** (`--resume` and `--session-id` both
  refuse; the lock is transcript-write concurrency). `tmux send-keys` does work but arrives
  indistinguishable from operator typing — rejected as a channel for that reason.
- Nothing ships that provides a broker (no MCP pub/sub reference server, no connectable
  supervisor endpoint); the agent-teams mailbox is experimental and Claude Code deletes
  entries it does not recognise. The filesystem is the broker we already have.

## Proposal

A one-way status channel, additive to everything that exists (sidecar, session log, close
handshake and gates all unchanged, so nothing can regress).

1. **Channel** — `$(git rev-parse --git-common-dir)/the-works/status/<feature>.jsonl`, one
   JSON object per line. In git-common-dir, so an architect in a worktree and an orchestrator
   in the main checkout share it with no path plumbing, and it stays uncommittable.
2. **Architect emits** one line per real transition: `started` · `loaded` · `developing` ·
   `spawning-agent` · `testing` · `blocked` · `finished` · `failed` · `abandoned`. The failure
   states are mandatory so a stalled or dead architect is never silent.
3. **Orchestrator absorbs** — at boot it spawns ONE background subagent which arms a
   `persistent` Monitor on the status directory, never returns, keeps a board, and messages
   the orchestrator only on actionable states. Progress ticks are absorbed silently.
4. **Re-arm at every renewal** — a fresh orchestrator has no absorber, and no absorber means a
   silently stale board.

Deliberately NOT included: any reverse channel (orchestrator → architect), which would require
either keystroke injection or a broker. See [[hook-choreography]], [[cross-repo-inbox]].

## Testing

Operator-agreed method — exercise the channel end to end before this closes:

1. Write status lines into a scratch status file, as an architect would.
2. Spawn a subagent that arms a Monitor on it and reports what it receives.
3. Verify: the subagent receives the events; the orchestrator receives NONE of the raw
   payloads (checked by a token that must not appear in the parent context); the subagent can
   push a digest up via `SendMessage(to: "main")`.
4. Verify the failure path: a `failed` line is delivered, not swallowed by the filter.

Pass = every check above observed live. "The code looks right" is not a pass.
