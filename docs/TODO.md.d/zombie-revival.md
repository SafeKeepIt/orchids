- created: 2026-07-21
- created_by: Sebastien Lambla

## Blockers

- None hard; builds on the merged [[message-bus]].

## Questions

- Is revival universal, or scoped to roles worth reviving (operator's example: a dead
  orchestrator)? A finished builder should presumably stay dead — though only top-level
  sessions hold inboxes (Decision-015), which may settle it by construction.

## Findings

- Operator spec (2026-07-21): delivery to a ZOMBIE (a session that died, e.g. an
  orchestrator that must be revived) is decided by SCRIPTS, not models — the delivery
  path checks whether the session id still has a live pid; if not, it restores the
  session BEFORE delivering. The respawn race is avoided by a LOCK on the session-id
  folder while respawning.
- Operator refinement (2026-07-21): NOTHING new is recorded at announce. The session id
  alone suffices — `claude --resume <session-id>` restores the session with its own
  context (the harness knows its project/worktree; resume is role-agnostic, so no
  per-role relaunch commands). The pid check is derived at delivery time from the live
  process table, not from announce-time bookkeeping.
- Lock shape ratified in-session: `flock` on the recipient's session-id folder — atomic
  (concurrent deliveries can't both respawn), kernel-held (no lockfile bookkeeping),
  auto-released on holder death (a crashed respawner can't wedge the inbox).
- Honours the no-scheduler ban ([[bus-liveness]]): the check runs only when a message
  needs delivering, never on a timer. Complementary split: [[bus-liveness]] = how death
  is evidenced; THIS task = what delivery does about it.

## Proposal

The bus delivery path gains a script-side liveness gate: under `flock` on the
recipient's session-id folder — is the session id's pid alive? If not,
`claude --resume <session-id>`; then unlock and deliver. Scripts decide everything;
models decide nothing.

## Testing

To agree when ripened — expected shape: kill a session, send it a message → the script
revives it (correct worktree, correct role, via resume) and the message arrives; N
concurrent sends to the same zombie produce exactly ONE respawn and N delivered
messages.
