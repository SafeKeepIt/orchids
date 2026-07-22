- created: 2026-07-22
- created_by: gh-ingest
- created_during: interactive

## Blockers
- None known yet.

## Questions
- Ingested from GitHub issue #92 — needs triage: type, component,
  urgency, scope.

## Findings
- Filed on GitHub (https://github.com/kaukea/orchids/issues/92); original body preserved below.

#agents #dependencies #frontmatter #role-delivery #install-flow #kauk

Two rulings, closing `agents-first-class`'s last open questions:

- **Agents declare dependencies on other agents**, not just on skills. The real graph
  has these edges (the orchestrator hands to architect/housekeeper/groomer; the
  architect dispatches builder), and an undeclared edge deploys a broken agent.
  Consequence for the two-page install flow: page 1 greys out agents required by a
  chosen agent, exactly as page 2 greys out required skills — the pull-in is legible,
  never silent.
- **The declaration is a `requirements:` frontmatter map with two sub-lists**, kinds
  explicit:

      requirements:
        agents: [builder]
        skills: [workflow, workflow-complete, handover]

  Chosen over a flat mixed list (would need a cross-folder uniqueness rule) and over
  typed ids (`agent:builder` — noisier). The map form takes a third sub-list later
  without disturbing these two — how `agent-external-deps` stays unprecluded while
  deferred.

Context, not ruling: the `roles:` key remains `role-dag-frontmatter`'s to settle; the
dependency contract no longer waits on it. The resolution/greying engine is kauk's
`agent-deployment`.
