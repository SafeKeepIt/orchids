---
name: skill-sync
description: "Keep this repo's skills, agents, and shared rule files aligned with the canonical template repo (src/serialseb/orchids) via `orchids-sync`. Run `status` at workflow start and end; report drift to the operator; `apply`/`pull` only on their go. Replaces the retired `dotai sync`."
metadata:
  tags: [ sync, skills, drift, canonical, orchids, template ]
  share: github
---

# Skill Sync

## Intent

Skills, role agents, hooks, board tools, and the shared rule files (`AGENTS.shared.md`,
`AGENTS.files.md`) are **cross-project and agent-tool-agnostic**, shared from ONE
canonical source: the template repo at `~/src/serialseb/orchids`. Each coding agent gets
only a thin adapter (Claude: `.claude/skills/` copies + a `CLAUDE.md` that injects the
AGENTS files; other tools' skill directories are added the same way). Files are **plain
copies** (no symlinks, no hidden clone directory — the predecessor tool `dotai` used
gitignored symlink targets and its loss orphaned every repo). `orchids-sync` compares
hashes and copies in either direction; this skill is the contract for when to run it and
what to do with drift.

## Checklist

- [ ] `orchids-sync status` run at workflow start
- [ ] `orchids-sync status` run at workflow end (before the close)
- [ ] Any drift reported to the operator — never silently overwritten in either direction
- [ ] Canonical-owned files changed in this repo: `pull` back to orchids on the operator's go
- [ ] Synced file changes committed in this repo (they are ordinary tracked files)

## Commands

```sh
orchids-sync status            # drift report for the current repo (or --all)
orchids-sync apply             # copy canonical → repo (missing files; drifted need --force)
orchids-sync pull <path>       # copy this repo's version of a file → canonical
orchids-sync init <dir> <profiles…>   # register a new repo and apply its profiles
```

Errors from `status` are ignored; the workflow proceeds regardless.

## Direction of truth

- **orchids is canonical.** A repo edits a shared skill only as a deliberate act, and the
  change is `pull`ed back to orchids (then `apply`ed outward) so the fleet never forks.
- **Project-specific overrides do NOT edit the shared file** — they go in the repo's
  `AGENTS.md` (e.g. signmc's "no `Co-authored-by` trailer" override of `git-commit`).
- `AGENTS.md`, `CLAUDE.md`, and everything outside the manifest are never touched by
  `apply` once they exist.

## Creating a new skill

Author it in **orchids** (`skills/<name>/SKILL.md`), following the `doing-skills` skill.
Add it to `manifest.conf` with its profile(s), then `orchids-sync apply --all` on the
operator's go. To draft privately, add it to no profile — it ships nowhere until listed.

## Mid-workflow drift

If `status` mid-workflow shows canonical moved under you, reload the changed skill, then
ask the operator whether to apply the change only from here on or to retrofit work
already done. Do not silently retrofit, do not silently ignore.
