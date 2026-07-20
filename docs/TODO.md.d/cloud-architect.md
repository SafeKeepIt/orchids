- created: 2026-07-20
- created_by: Sebastien Lambla

## Blockers

- ~~⊘handover-contract; both interactive boundaries parked the autonomous path~~ —
  OVERRULED (operator, 2026-07-20, Decision-027): "for cloud, there is absolutely no
  blocker." Waiting delays discovering the deviance in the system — start now. The
  contract is encoded; the gates apply INSIDE the flow (summary → MAKE IT SO; THAT IS
  ALL → housekeeper), they do not gate starting it.

## Questions

- First slice: the intake + ripening lanes on issues only (orchestrator + ripener
  rounds as issue comments, architect kicked off manually), or the full path through
  MAKE IT SO → pull request in one go?

## Findings

- **The design: TitanShield `docs/TODO.md.d/rework-task-lists.md`** (2026-07-01,
  operator-ratified). Key parts this task implements orchids-side: the AUTONOMOUS origin
  (`readiness = stage × origin`) with the strict self-authorize boundary, the shared
  close spine (review via auto-opened PR; THAT IS ALL stays the final gate; the
  housekeeper is the only writer to `main`, closing via `gh pr merge --squash`), and the
  verified cloud-trigger facts (routines ≥1h, `/fire` OAuth endpoint, `@claude` mention
  path; PR/Release-only routine triggers).
- **The cloud flow (Decision-027):** new feature = a GitHub issue → the orchestrator
  asks its intake questions before the task reaches the board proper → the ripener's
  functional-completeness rounds, all as comments on the issue (or a discussion —
  operator is indifferent) → statistical readiness reached → architect kicked off
  automatically → tech plan, few or no questions, summary → MAKE IT SO → pull request →
  THAT IS ALL → housekeeper amends + merges the PR. Locally the same spine runs on
  worktrees.
- Question economy (Decision-027): better questions upstream, fewer downstream; the
  current gates reflect today's error rate and shrink as upstream improves.
- The [[github-board-sync]] lane (issues mirror, Orchidarium Project, board-sync
  workflow) already gives the issue substrate and a cloud-triage precedent.

## Proposal

- (scope round in progress; first slice per the open Question, then the architect's
  tech plan under Decision-025/027)

## Testing

To agree when the first slice is scoped; must include one real feature taken through
the cloud path with every gate honoured (no self-approved MAKE IT SO, no self-approved
close).
