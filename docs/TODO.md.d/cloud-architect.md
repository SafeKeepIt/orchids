- created: 2026-07-20
- created_by: Sebastien Lambla

## Blockers

- ⊘[[handover-contract]] — operator: without a better-defined orchestrator→architect
  handover, "cloud agents will not work". To be delivered together, with strong gating.

## Questions

- ~~Where does the existing close-to-complete design live?~~ Located 2026-07-20:
  TitanShield `docs/TODO.md.d/rework-task-lists.md` (design `ready` 2026-07-01,
  implementation operator-deferred "just behind" active work).
- Which slice of the architect's job goes to the cloud first: analysis + question
  drafting only, or the full autonomous path (self-authorize → build → PR)?
- Relationship to the cloud orchestrator lane in [[github-board-sync]] (board-event
  triage on Actions): same runner infrastructure, or a separate cloud-agent mechanism?

## Findings

- Operator (2026-07-20): a close-to-complete design exists for using cloud agents to
  automate part of the architect's job — features that can be analyzed, questions asked,
  technical details sorted, then implementation done. Wanted SOON, and explicitly paired
  with [[handover-contract]] because the handover completeness is what makes an
  un-interactive agent viable.
- **The design: TitanShield `docs/TODO.md.d/rework-task-lists.md`** (2026-07-01,
  operator-ratified). Key parts this task implements orchids-side: the AUTONOMOUS origin
  (`readiness = stage × origin` — already adopted by our §TODO) with the strict
  self-authorize boundary (simple · no conflicts · no unknowns · questions answered), the
  shared close spine (review via auto-opened PR because no one is in-session; THAT IS ALL
  stays the final gate; the housekeeper is the only writer to `main`, closing via
  `gh pr merge --squash`), and the verified cloud-trigger facts (routines ≥1h, `/fire`
  OAuth endpoint, `@claude` mention path; PR/Release-only routine triggers). The
  "questions answered" boundary is exactly the [[handover-contract]] build-ready bar.

## Proposal

To be written once the existing design is located ([[handover-contract]] defines the
interface it plugs into).

## Testing

To agree at grooming; must include one real feature taken through the cloud path with
every gate honoured (no self-approved MAKE IT SO, no self-approved close).
