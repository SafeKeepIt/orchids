- created: 2026-07-20
- created_by: Sebastien Lambla

## Blockers

- None — this is the gating work the rest of the programme waits on.

## Questions

- ~~Does [[architect-delegation]] fold into this contract rewrite or stay its own task?~~
  FOLDED IN (operator, 2026-07-20) — that entry is cancelled-as-absorbed; its content
  lives here now.
- What is the completeness BAR for a build-ready sidecar — a checklist the orchestrator
  must satisfy (design settled, questions closed, test method agreed, size), enforced how?
- "Ask me all the questions before launching": collected from where — the sidecar's open
  Questions only, or also the ones grooming would surface? And batched in one round?
- (absorbed) What restores delegation trust: mandatory builder dispatch above a size
  threshold, evidence of delegation in the close-gate report, or a different contract
  shape? Does the contract stop permitting single-handed builds outright?

## Findings

- Absorbed from [[architect-delegation]] (2026-07-20): the operator does not currently
  trust the architect — the 2026-07-20 role-dag build dispatched 4 Haiku explorers in
  discovery but built every step single-handed. The architect definition PERMITS that
  ("directly or via parallel builders"), so the contract, not just the behaviour, is
  what needs tightening. Decision-023's deferred header-fill move re-evaluates when
  delegation trust is restored — the trigger now lives here.
- Operator (2026-07-20): the lines between orchestrator and architect are VERY BLURRED.
  Intended split — the ORCHESTRATOR owns task relationships (priorities, relative
  importance, functional relevance — e.g. warning that a feature has no consuming
  component), and owns getting the sidecar complete enough that the ARCHITECT thinks
  only about HOW to build, then dispatches coders. "Already supposed to be the case" —
  but not what happens (see [[architect-delegation]]: the 2026-07-20 build was
  single-handed).
- Before launching an architect the orchestrator asks the operator ALL open questions
  up front, and also offers parallel work: whether to launch additional tasks/architects
  at the same time ([[tmux-topology]] gives each its window).
- Hard consequence: [[cloud-architect]] cannot work without this contract — a cloud
  agent cannot ping-pong questions mid-flight, so the handover must be complete at
  dispatch. The operator wants the pair delivered together, with strong gating.

## Proposal

Define the orchestrator→architect handover as a CONTRACT: the build-ready bar for a
sidecar, the front-loaded question round, the parallel-launch offer, and what the
architect may assume on receipt (design done — HOW only). Encode it in the orchestrator
and architect definitions and the sidecar §format; enforcement per the bar Question.

## Testing

One feature taken through the new handover: every operator question asked in one round
before launch; the architect receives a sidecar it never has to bounce back for design
answers; a cloud-shaped dry run (no mid-flight operator contact) reaches MAKE IT SO
readiness on the sidecar alone.
