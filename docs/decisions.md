# orchids — decisions

Append-only. Grep by `#keyword`; read the TAIL, never the whole file.

## [2026-07-16] Decision-001: History migration is an orchestrator charter, gated by the AGENTS.md `repository:` field
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

## [2026-07-17 11:02 CEST] Decision-002: Delivery is driven by a task-oriented role DAG declared in the definitions
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

## [2026-07-17 11:02 CEST] Decision-003: The orchids role vocabulary
#roles #taxonomy #vocabulary #sync #forensics #workflow #general #process #security

**Context:** The concrete node list implementing Decision-002, decided against the
existing 26 skills. Supersedes nothing — `dev|infra|org|all` was never a decision,
just an artifact (kauk's auto-adoption stamps every adopted skill `dev`,
`bin/kauk:272`). Operator ruling (2026-07-17).

**Decision:** the node list is

```
general            read-agents · agent-behaviour · authoring-skills ·
                   git (generic half)
process
  └ workflow       workflow · workflow-complete · handover · groom ·
                   orchestrator · history-rewrite · readme-sync ·
                   git (workflow-specific half)
  └ (kanban)       reserved sibling slot — unbuilt, must stay expressible
development        clean-code · diagnostics
  └ dotnet         coding-dotnet
  └ tofu *         coding-tofu
  └ lmstudio       coding-lmstudio
  └ file-formats   shortcut-file · reverse-engineering-files *
infrastructure     software-catalog
  └ tofu *         coding-tofu
security           digital-signature
  └ forensics      chain-of-custody · forensic-acquisition · read-apfs ·
                   machine-access · icloud · reverse-engineering-files *
```

`*` = multi-parent (the DAG rule, Decision-002).

Rulings embedded in the above, each a choice among live alternatives:
- **`general` is not `core`.** "Core" implies mandatory, which is what smuggled one
  specific process into every repo. What is actually universal is ~700 bytes.
- **The workflow is a child of `process`, not a universal.** `handover`, `readme-sync`,
  `workflow-complete` and the `Branch:`/main-immutable git rules are *our* process, and
  a repo running a different one must be able to decline them.
- **`security` is the node; `forensics` is its child.** Matches SFIA, which files
  `Digital forensics (DGFS)` under Security services. We do not promote a leaf to a
  root. `digital-signature` sits at `security` — signing is not forensics-only.
- **`infrastructure`, not `operations`.** The corpus is IaC/provisioning and contains
  zero run-it-in-production skills. The two names overlap badly; pick one. (Noted:
  `infrastructure` is industry vernacular — Spotify, GitLab — not SFIA/NICE vocabulary.)
- **`git` splits** — generic hygiene (gitmoji, subject/body limits, scope discipline)
  is `general`; the `Branch:` trailer, main-immutable, and the MAKE IT SO gates are
  `process/workflow`.
- **`doing-skills` is renamed `authoring-skills` and sits in `general`.**

**Open, deliberately not ruled here:** `write-to-s3`'s placement. Provisionally
`security/forensics`, but the operator flagged it as likely carrying private
information that must not be published — a publication question, not a taxonomy one.
See TODO `pre-publication-cleanup`.

**Gap noted, not fixed:** `ARCHITECTURE.md` has no Taxonomy table, though
`AGENTS.files.md` §TODO requires `functionality`/`component` to draw from it and
`board_lint.py` lints `value ∈ glossary`. The board's `publication` / `process` /
`sync` values are de facto only.

## [2026-07-17 14:36 CEST] Decision-004: Agent dependencies — agent→agent edges are declared, in a `requirements:` map
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
