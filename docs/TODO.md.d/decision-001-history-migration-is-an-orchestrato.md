- created: 2026-07-22
- created_by: gh-ingest
- created_during: interactive

## Blockers
- None known yet.

## Questions
- Ingested from GitHub issue #89 — needs triage: type, component,
  urgency, scope.

## Findings
- Filed on GitHub (https://github.com/kaukea/orchids/issues/89); original body preserved below.

#history-rewrite #orchestrator #repository #orchids #gitflow #migration #subagent #parallel

**Context:** No role owned the `history-rewrite` skill — the orchestrator's
direct-on-main carve-out covered only the workflow component, and the architect's
scope is one feature sidecar, not every ref. Operator ruling (2026-07-16).

**Decision:**
- The orchestrator charters history migration — the one repo-wide surgery in its
  domain. No architect: the scope is the whole ref graph, not a feature.
- **Applicability gate:** the project `AGENTS.md` declares `repository:`. Only
  `orchids` (the canonical workflow shape; missing/empty counts as `orchids`) is
  eligible. Any other value (e.g. `repository: gitflow`) means the repo keeps its
  own branching model — agents never restructure its history.
- **Parallel prep, gated writes:** the skill's §0–§1 (sensitive sweep + partition
  proposal) are read-only and run as a background subagent while the orchestrator
  keeps working the board. All writes (§2+) wait behind operator gate #1; the
  partition, QES, and swap gates remain operator-only.

**Touched:** `agents/orchestrator.md` (new History-migration section),
`skills/history-rewrite/SKILL.md` (applicability gate + dispatch note),
`templates/AGENTS.md` (`repository:` convention).
