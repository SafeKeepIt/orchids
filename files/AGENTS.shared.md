# Shared agent instructions

This file contains shared instructions for all agents and all projects.

It MUST NOT be:
- modified
- deleted
- moved
- renamed

unless explicitly requested by the user.

---

## Core principles

- Any rule can be overruled by the user
- The user's architecture, requirements, and designs are mandatory
- The agent MAY propose changes but MUST NOT apply them without user approval.
  The following always require surfacing the choice and waiting before acting:
  - **Scope expansion** — anything outside the agreed workflow scope.
  - **Destructive or hard-to-reverse operations** — file deletes, overwrites of
    uncommitted work, force push, `reset --hard`. Git-specific destructive operations
    are governed by the `git-commit` skill; branch deletion is handled by the
    workflow + worktree pattern (branches are immortal).
  - **Technology, library, tool, or approach choice** when more than one option is
    viable. Per-technology skills carry the stack-specific defaults; surface the
    choice when no skill settles it.
  - **Spec decisions not yet set** — defaults, parameters, paths, naming.
  - **Actions visible outside the conversation or affecting shared state** — deploys,
    PR/issue actions, messages to others, pushes to shared branches.
- When the agent has multiple questions to settle, list the question titles first as
  a numbered preview, then ask each question independently, waiting for the operator's
  answer before moving to the next.

---

## Mandatory files

### README.md

Describes the repository for humans.

Rules:
- Uses sections starting with `# <header>`
- Only update sections impacted by your changes. In the case of a mono repo, only update the part of the file related to your changes' area.

Must include:
- WHAT the repository does (intent, not implementation), max 5 lines
- Installation instructions
- Usage example (end-to-end, concise; may include comments)

---

### AGENTS.shared.md

- Shared instructions across all projects
- MUST NOT be modified unless explicitly requested

---

### TODO.md

The project's pipeline for upcoming work.

- New items surfaced in any conversation — follow-ups, parked thoughts, future ideas, side-quests —
  are added here when they surface, not held in memory and not deferred.
- Pull from `TODO.md` before pulling from model memory or chat-only context.
- Completed items move to `DONE.md`. They are never deleted.
- Workflow-specific operational steps live in the `workflow` skill for projects using it.

---

### DONE.md

The source of truth for completed work — cheaper to read than reconstructing from git history.

- Append-only.
- Populated only by moving items out of `TODO.md` on completion.
- Grouped by date. Each date has a one-line summary of all changes for that day, then a list of the
  individual changes.
- Workflow-specific entry format (e.g. squash titles as the change identifier) lives in the
  `workflow` skill for projects using it.

---

## Repository structure

- Group files by technology
- Source code MUST be in `src/`
- Tests MUST be in `tests/` when applicable

Example:

/
  python/
    src/
    tests/
  opentofu/
    src/

---

## Software principles

- SOLID
- KISS
- Do NOT write speculative code or scope beyond the current feature
- Prefer self-descriptive code over comments

---

## Editing rules

- Keep changes local unless broader changes are required
- Do NOT change architecture without user approval
- Reuse existing patterns before introducing new ones

---

## Tone

How the agent talks and interacts with the operator.

- **Helpful, not ordering around** — guide and support; do not issue commands.
- **Concise** — no piling on context; one focused answer per response.
- **Direct about what was done vs skipped** — no euphemisms ("simplified",
  "streamlined", "for now").
- **No trailing summaries unless asked** — do not restate the diff or relist
  approved bullets.

---

## Agent boundaries

The agent observes infrastructure state and reports it. It does not declare a remote, ref, file, or
service "stale", "broken", "unreachable", or "wrong" as grounds for skipping or rewriting a workflow
step. Those calls are the operator's. If observed state conflicts with the workflow, the agent stops
and reports what it sees, and asks how to proceed.

---

## Stop condition

Stop when:
- the requested change is complete
- the result is sufficiently verified for the task
