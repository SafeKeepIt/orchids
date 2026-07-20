---
name: authoring-skills
description: How to author, structure, and publish a skill for this fleet of repositories. Read before creating or materially restructuring any SKILL.md. Defines the frontmatter contract, the canonical section order (Intent, Checklist, Rules, worked example), the one-skill-one-concern rule, and the kauk publishing flow.
metadata:
  tags: [ skills, authoring, skill, meta, template, frontmatter ]
  share: github
---

# Authoring skills

A skill is a contract the agent loads on a trigger — not documentation, not a tutorial.
Skills are **cross-project and agent-tool-agnostic**: author them in the canonical repo
(`~/src/serialseb/orchids/skills/<name>/SKILL.md`), never in one project's tool
directory, and ship them with `kauk sync` (see the `kauk` skill).

## Checklist

- [ ] Frontmatter: `name` matches the folder; `description` states the TRIGGER, not just the topic
- [ ] One concern per skill — split rather than grow a second concern
- [ ] Sections in order: Intent → Checklist → body/Rules → worked example (where it earns its place)
- [ ] Checklist items are observable, tickable steps — not restated prose
- [ ] No duplication of `AGENTS.shared.md` / `AGENTS.files.md` — reference them (`§TODO`, `§Decisions`)
- [ ] Nothing tool-specific (no Claude-only paths or commands) unless the skill is about that tool
- [ ] Added to `manifest.conf` as `skill <name> <role>` (`dev` · `infra` · `org` · `all`)
- [ ] `kauk sync` run on the operator's go

## Frontmatter contract

```yaml
---
name: <folder-name>                  # MUST equal the directory name
description: <when to load it — the trigger — then what it does, one flowing sentence(s).>
metadata:
  tags: [ <grep-able trigger words> ]
  share: github                      # present on every fleet-shared skill
---
```

The skill's role (`dev` · `infra` · `org` · `all`) lives in canonical `manifest.conf`,
fixed by us; repos tune delivery in their `.ai.toml` (see the `kauk` skill).

The `description` is what the model sees when deciding whether to load the skill — write
it as trigger-first ("Use whenever…", "MUST be read before…"), because that is the whole
selection mechanism. A placeholder description is a bug: the skill will never fire.

## Body shape

1. `# Intent (<name>)` — one short paragraph: what this is for, when it applies.
2. `## Checklist` — the boxes the agent ticks while following the skill.
3. Rules / procedure sections — short imperatives; bold the **MUST/NEVER** verb.
4. A worked example where one earns its place (the `software-catalog` incident block,
   `readme-sync`'s sample README) — a real example beats abstract prose.

## Rules

- **Trigger-first descriptions.** The description sells the trigger; the body carries the
  procedure.
- **One concern.** A skill that needs "and also…" is two skills.
- **Reference, don't restate.** Formats live in `AGENTS.files.md`; principles in
  `AGENTS.shared.md`. A skill that copies them will drift from them.
- **Encode incidents.** When a real failure taught a rule (purge cascade, FUSE
  false-empty), keep the concrete incident in the skill — it is the proof the rule earns
  its cost.
- **The operator may override any skill per session** — say so only when the skill gates
  something; it is the default everywhere.
- **Publication is per-skill, and the CASE is never in it.** The incident/case data
  (`case-file/`, evidence, anything about the operator's specific event) is **permanently private** —
  it never enters a shared/`github` repo. Skills DEFAULT to publishable (`share: github`), with ONE
  exception: a skill whose technique could carry **LEGAL RISK** — access-circumvention, credential
  testing, forensic machine access, cloud-account data pulls (e.g. `machine-access`, `icloud`) — must
  be **individually reviewed for legal exposure BEFORE** it is marked `share: github`. Only those
  skills need the review; the rest publish normally. Until reviewed, a risky skill stays **unshared**
  (no `share: github`).
