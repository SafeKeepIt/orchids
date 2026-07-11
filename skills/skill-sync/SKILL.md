---
name: skill-sync
description: "Keep this repo's skills, agents, and shared rule files aligned with the canonical source repo (src/serialseb/orchids) via the `orchids` CLI. Run `orchids sync` at workflow start and end. Delivery per skill is tuned in .ai.toml (exclude|copy|link|local). Replaces the retired `dotai sync`."
metadata:
  tags: [ sync, skills, drift, canonical, orchids, template ]
  share: github
---

# Skill Sync

## Intent

Skills, role agents, hooks, board tools, and the shared rule files (`AGENTS.shared.md`,
`AGENTS.files.md`) are **cross-project and agent-tool-agnostic**, shared from ONE
canonical source repo at `~/src/serialseb/orchids`, checked out per-project at
`.ai/repositories/serialseb/orchids/` (only `.ai/repositories/` is gitignored) and laid
into the project as **absolute symlinks** — absolute so git worktrees resolve them. You
CAN write through a symlink: Edit/Write follow them transparently; edit the skill at the
path you loaded it from, never chase the target into `.ai/repositories/`. `orchids sync`
is git doing the magic: local edits are committed in the checkout, rebased onto
canonical, pushed back — every project converges.

## Checklist

- [ ] `orchids sync` run at workflow start
- [ ] `orchids sync` run at workflow end (before the close)
- [ ] Rebase conflicts resolved with the operator — never silently, in either direction
- [ ] UPDATE/DRIFT notices for `local`/`copy` skills surfaced to the operator
- [ ] Symlink or `.ai.toml` changes committed in this repo like any tracked file

## Commands

```sh
orchids init             # one-time: clone, migrate existing files, lay symlinks
orchids sync             # commit local skill edits → rebase on canonical → push back
orchids sync --status    # readable drift/ahead-behind report
```

Errors from `sync` are ignored for the workflow's purposes; it proceeds regardless.

## Delivery config — .ai.toml

Per-repo, at the repo root, written by the CLI (never hand-edited; agents drive it via
this skill). **Missing or empty = every skill installed as a link.** Otherwise `[dev]` /
`[infra]` / `[org]` / `["*"]` sections with `skillname = "exclude"|"copy"|"link"|"local"`:
`exclude` = not installed · `copy` = real file, drift reported, never overwritten ·
`link` = symlink (default) · `local` = the repo's own version, NEVER sent back to the
source, canonical updates announced at sync. A skill's role is fixed in canonical
`manifest.conf`; `.ai.toml` only tunes delivery.

## Creating a new skill

Author it in **orchids** (`skills/<name>/SKILL.md`), following the `doing-skills` skill,
add `<name> <role>` to `manifest.conf`, then `orchids sync`. Repo-born skills are adopted
into canonical automatically by `orchids init` (unless marked `local`).

## Mid-workflow drift

If a sync mid-workflow pulls a changed version of a skill you already loaded, reload it,
then ask the operator whether to apply the change only from here on or to retrofit work
already done. Do not silently retrofit, do not silently ignore.
