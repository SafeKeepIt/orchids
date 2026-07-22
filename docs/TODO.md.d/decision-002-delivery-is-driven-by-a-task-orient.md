- created: 2026-07-22
- created_by: gh-ingest
- created_during: interactive

## Blockers
- None known yet.

## Questions
- Ingested from GitHub issue #90 — needs triage: type, component,
  urgency, scope.

## Findings
- Filed on GitHub (https://github.com/kaukea/orchids/issues/90); original body preserved below.

#roles #taxonomy #delivery #frontmatter #manifest #kauk #sync #context-economy #install

**Context:** Every session in every repo loads all 26 skill descriptions (~10.2 KB)
whether or not the work is relevant. `manifest.conf` already carries a `role` field
(`dev|infra|org|all`), but it is **inert**: kauk's `resolve_mode` (`bin/kauk:41-56`)
reads it only as a section name to look up in `.ai.toml`, never as a filter, and no
`.ai.toml` in the fleet defines a role section — so all 26 skills link everywhere.
Agents are worse: plain `link` lines, installed unconditionally with no identity.
Operator ruling (2026-07-17).

**Decision:**
- **Roles are task-oriented, never job titles** — `development`, not `developer`.
  Follows SFIA 9 (activity-noun categories) and NICE/NIST SP 800-181, which renamed
  its whole vocabulary in 2023 explicitly "to avoid being mistaken for job titles".
- **Authors declare the role, in the skill/agent definition's frontmatter** — not in a
  central table. The author of a skill knows what it is for; `manifest.conf`'s role
  field is retired as the home for this.
- **Roles form a DAG, not a flat list.** Nodes nest (`security` → `forensics`); a
  definition may declare several paths (`coding-tofu` is genuinely both
  `development/tofu` and `infrastructure/tofu`). A flat list forces false choices and
  presents one specific process as universal.
- **Selection installs the chosen node's subtree**, plus its ancestors' own skills.
  A node with children is selectable as the coarse pick.
- **Agents become first-class and may declare required skills** — a dependency the
  package can state, rather than an assumption (e.g. the workflow needs the groomer).
- **The HOW is kauk's, not orchids'.** orchids ships the vocabulary, the declarations
  and the dependency edges; the reader, the install-time picker, and the filter are
  kauk's. orchids is data-only, so this work lands as data even while kauk ignores it.
- **The vocabulary must not preclude unbuilt siblings** (e.g. a `process/kanban` beside
  `process/workflow`). Not built now; not designed out either.
