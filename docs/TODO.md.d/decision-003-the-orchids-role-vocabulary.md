- created: 2026-07-22
- created_by: gh-ingest
- created_during: interactive

## Blockers
- None known yet.

## Questions
- Ingested from GitHub issue #91 — needs triage: type, component,
  urgency, scope.

## Findings
- Filed on GitHub (https://github.com/kaukea/orchids/issues/91); original body preserved below.

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
