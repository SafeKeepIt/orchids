- created: 2026-07-20
- created_by: Sebastien Lambla

## Blockers

- ~~⊘handover-contract; both interactive boundaries parked the autonomous path~~ —
  OVERRULED (operator, 2026-07-20, Decision-027): "for cloud, there is absolutely no
  blocker." Waiting delays discovering the deviance in the system — start now. The
  contract is encoded; the gates apply INSIDE the flow (summary → MAKE IT SO; THAT IS
  ALL → housekeeper), they do not gate starting it.

## Questions

- ~~First slice?~~ RULED (operator, 2026-07-20): the FULL PATH to PR in one slice —
  the whole spine surfaces its deviance at once.

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

First slice = the FULL PATH (operator, 2026-07-20): a GitHub issue carries the feature;
the orchestrator's intake and the ripening rounds run as issue comments (driven manually
until the ripener charter lands); the architect is kicked off; tech plan with few or no
questions; the summary question → MAKE IT SO → pull request; THAT IS ALL → the
housekeeper amends and merges the PR. The local worktree spine is untouched. HOW —
Actions wiring, kick-off mechanics, the PR close path — is the architect's tech plan,
not pre-decided here (Decision-025/027).

## Testing

To agree when the first slice is scoped; must include one real feature taken through
the cloud path with every gate honoured (no self-approved MAKE IT SO, no self-approved
close).
