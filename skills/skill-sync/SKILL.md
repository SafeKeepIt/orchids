---
name: skill-sync
description: "Run `dotai sync` to keep this repo's skills aligned with their source clones. Read at workflow start, at workflow end, and on every code change in between. Errors are ignored. Required for skills with `share: github`."
metadata:
  share: github
---

# Skill Sync

## Intent

Skills are shared across projects via `dotai sync`, which lays them down as symlinks into each model's skill directory (`.claude/skills/`, `.opencode/skills/`, …). This skill is the contract for keeping that sync coherent — when to run it, how to author new skills, what to do when sync pulls changes mid-workflow, and what to commit afterwards.

## Checklist

- [ ] `dotai sync` run at workflow start
- [ ] `dotai sync` run on any code change in between
- [ ] `dotai sync` run at workflow end
- [ ] New or moved symlinks committed
- [ ] Mid-workflow sync changes — user asked how far back to apply them

## When to sync

At workflow start, at workflow end, and on every code change in between (commit, edit, refactor — anything that touches source). Errors from `dotai sync` are ignored; the workflow proceeds regardless.

## Creating a new skill

Use `dotai skills new <name> [<owner>/<repo>] [--batch]` to scaffold — never hand-create the folder. The tool writes `SKILL.md` with the right frontmatter, body sections, and `draft: true`, then auto-runs sync. While `draft: true` is set, the skill is symlinked under `.drafts/<name>` and is invisible to every model, so iteration is free.

## Publishing a draft

Delete the `draft: true` line from the SKILL.md you've been editing, then run `dotai sync`. The `.drafts/<name>` symlink retires and `.claude/skills/<name>` (plus the equivalent for every other configured model) is created.

## Editing a skill

Edit the skill at the path you loaded it from — `.claude/skills/<name>/SKILL.md`, or `.drafts/<name>/SKILL.md` for drafts. Never chase the symlink target into `.ai/repositories/<clone>/...`, and never edit another model's copy of the same skill. The Edit/Write tools resolve symlinks transparently; claiming you can't is wrong.

## Reloading after a mid-workflow sync

If `dotai sync` between workflow start and end pulls a changed version of a skill the model has already loaded, reload the new content immediately. Then ask the user whether to apply the change only from here on, or to also revisit work already done in this workflow and retrofit it. Do not silently retrofit, do not silently ignore.

## Committing the symlinks

`dotai sync` lands its changes as symlinks under `.claude/skills/`, `.drafts/`, and the `AGENTS.shared.md` symlink at the root. Their targets live under `.ai/repositories/`, which is gitignored — unstaged symlinks vanish on a fresh clone. Stage them.

When a workflow only changes skills (no other code), the symlink updates still need committing — the easy failure mode is finishing the workflow having committed nothing. Ask the user whether the symlink changes should ride along in the workflow's main commit/squash or land as a separate commit; either is fine, neither is automatic.
