---
name: workflow
description: MUST be read before starting any task, plan, or coding work, and again when finishing. Defines branch rules, commit format, merge procedure, and cleanup steps. No work begins or ends without following this.
tracked: true
metadata:
  tags: [ git, workflow, start, begin, task, plan, branch, finish, complete, end, merge, squash, cleanup ]
  share: github
---

# Intent (Workflow)

Any task, plan, workstream, or other set of tasks a coding agent executes sequentially for the user is called a workflow
and must follow those instructions.

## Checklist

The whole workflow must be followed, you must complete all these steps.

Workflow Start:

- [ ] Working tree resolved with user
- [ ] Skills synchronized
- [ ] Git commit format understood
- [ ] Feature branch and initial commit created

Workflow End:

- [ ] Completed testing
- [ ] User approval received
- [ ] Updated required documentation
- [ ] Tree cleaned
- [ ] Created marker tag
- [ ] Merged squash
- [ ] Verified integrity
- [ ] Feature branch deleted

## Rules

- Any work MUST follow these rules unless user override
- work MUST NOT start writing code until all conditions in workflow start have been executed

# Workflow start

A workflow is called differently in different agents: plans, tasks, workstreams, or others. They are all synonyms.

As soon as the user indicates the start of a new workflow, the workflow has started and you must follow the rules of the
workflow start immediately.

- work never starts on a dirty tree. Ask the user for confirmation to stash dirty files, do a WIP git commit, or treat
  the current state as a completed workflow and end it before starting the new one.
- all work MUST be done on a feature branch named `f/<feature-id>`.
- a feature branch MUST ONLY branch from the `main` branch, never from another feature branch.
- Merge commits during a workflow are forbidden, unless overruled by the user.
- Feature branches are required. The user MAY explicitly override for a given workflow to allow direct commits on
  `main` (or another non-`f/` branch). Absent that override, the feature-branch rule is absolute.

## Workflow Preparation

As soon as a user indicates wanting to start a workflow:

- Synchronize the skills
- Use the description provided by the user or ask for the user for a short intent.
- Create a feature branch `f/<feature-id>` from the latest `main` branch. The `<feature-id>` should be a concise,
  human-readable identifier for the work being done (e.g., `f/add-login-feature`, `f/fix-payment-bug`,
  `f/refactor-auth-module`).
- Create a commit describing the intent of the future branch, and a trailer called `Base` with the SHA of the commit
  from which the branch was created. with a `tada` gitmoji. This commit serves as the anchor for the branch and the
  starting point for all future work in this workflow.

# Workflow end

A workflow can only end once every item on the Workflow End checklist is satisfied. The Testing and User approval
gates below are non-negotiable; the model may not self-approve either.

Ending the workflow must follow the following steps in this order.

## Testing

Testing is the agreed method, between user and model, of ensuring a feature is complete and behaves as the workflow
described. The model and user must agree on a methodology appropriate to the change, and the model must have run it
and reported the results before the workflow can end.

Examples — pick what fits the change:

- Unit tests for new or modified logic
- Integration tests for cross-component behaviour or external boundaries
- Manual testing — a run-through to verify the workflow's functionality, which need not be committed (a transcript,
  screenshot, or described outcome is enough)

The model is encouraged to propose the most appropriate test for the feature, rather than wait to be asked. Once the
user agrees on the methodology, the model may carry it out autonomously instead of re-asking at each step.

## ⛔ User approval gate

STOP. The workflow MUST NOT proceed past this point without explicit user approval.

Provide a single concise summary, then wait for the user to reply with `MAKE IT SO`. Do NOT begin documentation
updates, tag creation, merge, or branch cleanup until the user has typed that exact phrase. "Looks good", "thanks",
or a thumbs-up is NOT approval.

The summary MUST:

- Fit on roughly one screen — bullet points, not prose. Don't re-narrate the diff.
- Cover every change against the agreed workflow:
  - Features implemented as agreed
  - Features modified, descoped, or skipped — with the reason
  - Shortcuts taken: mocks, hardcoded values, suppressed errors, disabled checks, skipped validation, TODOs left in
    code
  - Decisions made without consulting the user
  - Anything in the diff that does not match the workflow's stated intent
- Disclose problems encountered: failed approaches, dead ends, partial fixes
- State honestly what was NOT tested or what testing was skipped
- Propose the squash title for the merge step, so the user can approve it now

The model MUST NOT:

- Claim a feature is complete when it is partially implemented
- Hide shortcuts behind euphemisms ("simplified", "streamlined", "for now", "minimal version")
- Omit changes that fell outside the agreed workflow
- Wait for the user to ask about a known issue — surface it proactively


## Documentation Update

Update the project's agent-facing state on the feature branch, in a commit that the squash will carry to `main`. Do
NOT create a separate commit on `main` after the merge — the squash already lands these files, and an extra commit
pollutes history.

- [ ] Memory and documentation files must be reviewed to reflect the current state of the project, discarding
      out-of-date information.
- [ ] Agreed work, follow-up work, and future work must be updated in `TODO.md`. Completed items are removed from
      `TODO.md` and added to `DONE.md`.
- [ ] An entry must be appended to `DONE.md` for every workflow, using the squash title the user approved at the gate
      and a short summary. Format example follows.

`README.md` is for human users of the project and is NOT part of the workflow's mandatory update list. Touch it only
when the workflow genuinely changes user-facing behaviour and the user asks for it.

```yaml
# Completed work

[date] `<short summary of all changes that day>`
- `<git merge squash title 1>`
- `<git merge squash title 2>`
- `<git merge squash title 3>`
---
```

## Clean tree

Agents leave files behind tracking their work.

If files are included by .gitignore as preserve `!<path>` or ignore `<path>`, they are to be commited, otherwise alert
the user and propose adding the directory or the file to `.gitignore`, with a recommendation.
Examples:

- OpenCode plan files (`.opencode/plans/`, `plan.md`, or similar)
- Agent task files, scratchpads, or temporary reasoning files created by the tool
- Any file the tool created to track its own progress, not for the project
- Propose to the user to add any such file to the `.gitignore` file
- Do not delete files without user confirmation

Task files always get committed:

- `HANDOVER.md` — cross-session context for the next agent
- `TODO.md` — project-level work tracking yet to do. Move completed tasks to `DONE.md`
- `DONE.md` — project-level work done.
- `AGENTS.shared.md` and all symlinks coming from the `.ai` directory — they are shared rules.
- Memory files under `.claude/projects/` that are still relevant. Delete obsolete ones before committing.

## Marker tag

You must add a tag named `archive/<feature-id>` to the feature branch you're merging.

## Merge squash

Before merging, record the commit count of the feature branch:

```
N=$(git rev-list main..f/<feature-id> --count)
```

You must merge squash the feature branch onto the `main` branch, following this template.

```
<gitmoji> <subject>

🎯 <branch-head> 📦 <commits> ⌛ <lead-time>

<body>

Branch: <branch>
Head: <branch-head>
Co-authored-by: <model> <junie@serialseb.com>
```

- `<branch-head>` — Short SHA of the feature branch HEAD (the same commit that `archive/<feature-id>` tags).
- `<commits>` — Number of commits squashed.
- `<lead-time>` — Human-readable lead time (e.g., "2d 8h", "1m 2d") between the first commit of the feature branch and
  the merge commit. NOT measured from the commit you branched off of on `main`.
- `<branch>` — The feature branch you are merging.
- For anything else follow the rules in the git-commit skill.

After creating the squash commit, write the commit count as a git note on the new HEAD:

```
git notes add -m "commit-count: $N"
```

When pushing, always include notes so CI can read the count for versioning:

```
git push origin main refs/notes/commits
```

## Verify squash integrity

After the squash commit, verify that no content was lost and the metadata is correct:

```bash
# Tree content must match
SQUASH_TREE=$(git rev-parse HEAD^{tree})
BRANCH_TREE=$(git rev-parse archive/<feature-id>^{tree})
[ "$SQUASH_TREE" = "$BRANCH_TREE" ] || echo "ERROR: tree mismatch"

# Commit count must match rev-list
NOTED_COUNT=$(git notes show HEAD 2>/dev/null | grep commit-count | cut -d' ' -f2)
ACTUAL_COUNT=$(git rev-list $(git merge-base main~ archive/<feature-id>)..archive/<feature-id> --count)
[ "$NOTED_COUNT" = "$ACTUAL_COUNT" ] || echo "ERROR: commit count mismatch (noted=$NOTED_COUNT actual=$ACTUAL_COUNT)"
```

If either check fails, do NOT delete the branch. Investigate and fix the squash commit first.

## Delete branch

Delete the feature branch. Use `git branch -D` (force) because squash merges do not preserve ancestry — git's `-d`
safety check will always report "not fully merged" even when the content is identical. The archive tag and the integrity
check above are the safety net.
