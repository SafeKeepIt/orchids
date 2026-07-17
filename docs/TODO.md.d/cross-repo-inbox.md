- created: 2026-07-17
- created_by: opus-4.8

## Blockers
- None technically. But the sensitive-content rule (`AGENTS.shared.md`) constrains the
  design hard and must be settled before any format is fixed — see Questions.

## Questions
- **Push or pull?** Sender writes into the receiver's tree (needs the checkout on-box
  AND write access to someone else's repo), or sender writes an *outbox* in its OWN
  repo and the receiver pulls. Pull is the safer default — nobody writes another repo's
  tree, which is the exact failure this task exists to prevent — but it needs the
  receiver to know where to look.
- **Committed or uncommittable?** `HANDOVER.md` lives in `.git/` because it carries
  chatter and sensitive content. A cross-repo *requirement* is durable technical state,
  which argues for a committed path. But a message from a forensics repo could carry
  incident detail, and `AGENTS.shared.md` forbids sensitive content entering git history
  anywhere. Possibly two channels, possibly a hard "sanitized only" gate on the inbox.
- **Ingest-and-delete, or durable + acknowledged?** HANDOVER is deleted on sight. A
  requirement should probably become a task on the receiver's board and *then* the
  message dies — that is a different lifecycle, with an ack the sender can observe.
- **Who ingests, and when?** Receiving orchestrator at boot is the obvious hook (it
  already ingests HANDOVER there). Cost: another boot-time read on a role that is
  deliberately lean.
- **Sensitive content: ENCRYPTED AND KEPT, not deleted** (operator ruling, 2026-07-17).
  Delete-and-sanitize was considered and rejected: a message that warrants a task is
  persistent by definition, so destroying it destroys what the task needs.
  "Sensitive but not persistent" is an incoherent category. The orchestrator encrypts
  sensitive information at board grooming; `content: sensitive` marks content to
  **encrypt**, not to delete. Open below — this ruling sets the direction, not the
  mechanics:
  - **This contradicts a hard rule in an immutable file.** `AGENTS.shared.md` says
    sensitive content NEVER enters git history and goes ONLY to the uncommittable
    `.git/` channels. Committing ciphertext is sensitive content entering history —
    satisfying the rule's *intent* (nothing readable leaks) while breaking its *letter*.
    That file MUST NOT be modified without an explicit operator request. Needs a ruling
    before anything is built.
  - **Encrypted to whom?** The architect implementing the task must read it, so the key
    has to be reachable by an agent. That means this does not defend against a local
    attacker — it defends against *publication*. Naming the threat model decides the key
    choice: an operator smart-card key (strong, but every read needs a PIN — gpg
    Pinentry already timed out mid-session on 2026-07-17) vs a repo-local key (agent-
    readable, publication-safe only).
  - **Granularity:** whole sidecar encrypted, or marked blocks inside a plaintext
    sidecar? Blocks keep the board greppable and the task renderable; whole-file is
    simpler and leaks less metadata.
  - **Publication interaction, unresolved:** orchids is heading for publication
    (`pre-publication-cleanup`, urgent). Ciphertext committed now is ciphertext
    published later, permanently. If sensitive tasks are instead confined to the private
    side of that split, the encryption question may narrow considerably — decide the
    split first, or at least alongside.
  - Grooming is done by the `groomer` agent as well as the orchestrator; both need this,
    or the rule has a hole.
- **Whose component is the transport?** The protocol and the rules are orchids
  (workflow component). If delivery needs more than a shared filesystem or a git remote,
  that is kauk `federation` — and per its own rule, it gets filed on kauk's board, not
  specified here.

## Findings
- **There is no channel today, and its absence caused a real boundary violation on
  2026-07-17.** orchids decided the role-DAG model and needed kauk to build the reader.
  With no protocol, the orchids orchestrator wrote a task directly into kauk's working
  tree — authoring on a board it does not own, setting another project's badge,
  component, and priority. Operator ruling on the correction: work to be done by kauk
  *belongs* in kauk's repo (moving it there is right; deleting it would lose it). What
  was missing was a legitimate way to deliver it.
- **`HANDOVER.md` is NOT the precedent — it is a different process** (operator,
  2026-07-17). It exists so a subagent can hand information back to its agent: **one
  way, one round, every time**, then dead. It is uncommittable because of that
  **lifecycle** — nothing in it needs to survive, and it is never the input to creating
  a piece of work — NOT because of a sanitization policy. Reasoning "handover is
  uncommittable, therefore inbox messages are too" is a false analogy and was made once
  already in this task's history; do not make it again.
- **The inbox inverts every one of those properties.** Peer↔peer, not subagent→agent.
  Durable, not one-round. And it exists precisely to be the input that creates work on
  the receiver's board — which is why the content must persist, and why deleting it
  after a sanitized rewrite destroys the point of sending it.
- **Board edges are single-board by construction.** `⊘`/`~` ids are resolved by
  `board_lint.py`'s no-orphan-subtasks rule against entries on the same board, so a
  cross-repo dependency is unexpressable and unlintable. Today orchids' `role-delivery`
  → kauk's `role-aware-delivery` gate survives only as prose in two Findings sections.
  Both boards are one `git pull` from forgetting each other, and nothing will complain.
- kauk already carries a `federation` functionality (auth-broker, backends). If this
  ever needs transport beyond an on-box path, that is where it lives.

## Proposal
Sketch only — the push/pull and sensitive-handling forks above decide the shape, and
they are the operator's. Leading candidate: each repo owns an **outbox** of sanitized,
addressed messages; the receiving orchestrator pulls at boot, converts each into a task
on its own board, and acks. The sender never writes the receiver's tree. Message kinds
worth distinguishing early: *requirement* (do this), *knowledge* (this is true, you will
need it), *ack* (filed as `<id>`).

Fixed by operator ruling (2026-07-17), not open:
- **The inbox does NOT inherit the handover's rules — it is a different process.**
  See Findings for why. The `.git/`-only rule is a consequence of the handover's
  lifecycle, not a general sanitization policy to be copied here.
- **Sensitive content is encrypted and kept**, because it is the input to creating work.
- **External blockers are resolved when the orchestrator loads its tasks** — see the
  sibling task `external-blockers`, which owns that half.

## Testing
Two scratch repos: A posts a requirement to B; B's orchestrator boots, files it as a
real task on its own board, and acks; A observes the ack. Assert A never wrote to B's
tree. Negative test: a message carrying sensitive content is refused, not merely warned
about. Board lint stays clean on both sides throughout.
