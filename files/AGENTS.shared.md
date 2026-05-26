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

### TODO files

Per-component task tracking lives at `docs/TODO.<component>.md`, one file
per top-level component. A cross-cutting `docs/TODO.md` carries items that
don't fit a single component (repo-wide concerns: tracing, doc layout,
etc.). The fixed component list lives in the project's `AGENTS.md`; agents
do not invent new components.

Pull from these files before pulling from model memory or chat-only
context. New items surfaced in any conversation — follow-ups, parked
thoughts, future ideas, side-quests — are added here when they surface,
not held in memory and not deferred.

Each task is a `## <Title> {#kebab-case-id}` block. Metadata is a
nested-bullet block immediately under the heading. Free-form markdown
follows.

```markdown
## <Task title> {#<task-id>}

- id: <kebab-case slug, unique within file>
- type: bug | feature | refactor | housekeeping | completion
- status: todo | doing | blocked | paused | functional | done | cancelled
- created: <YYYY-MM-DD>
- created_by: <operator name OR model-version slug (e.g. opus-4.7) OR `unknown`>
- created_during: <workstream feature-id, e.g. f/foo>
- subcomponent: <free-form per-component label>
- parent: <markdown cross-reference>
- subtasks:
  - <markdown cross-reference>
- blocked_by:
  - <markdown cross-reference>
- completed: <YYYY-MM-DD>
- completed_during: <workstream feature-id>

<free-form markdown body>
```

**Omit fields with no value.** Empty arrays, null values, and unset
optional fields don't appear in the block.

**Required fields** (always present): `id`, `type`, `status`, `created`,
`created_by`.

**Conditional fields**:
- `completed` + `completed_during` — required iff `status ∈ {done, cancelled}`.
- `created_during` — omit if surfaced outside a workstream.
- `subcomponent`, `parent`, `subtasks`, `blocked_by` — omit if not applicable.

**Status semantics:**
- `todo` — not started.
- `doing` — active workstream owns it.
- `blocked` — gated; `blocked_by` lists what's in the way.
- `paused` — deliberately deferred without an active blocker.
- `functional` — works in current state, unfinished against full intent
  (e.g. waiting on other components, needs `completion`-type follow-up).
- `done` — no longer needs revisiting to meet its original spec.
- `cancelled` — decided against; rationale lives in the prose body.

**Type semantics:**
- `bug` — broken behavior to fix.
- `feature` — new capability. Can have subtasks (workflows).
- `refactor` — restructure without behavior change.
- `housekeeping` — cleanup, removal, doc tidy.
- `completion` — work that takes a `functional` feature to `done`.

**Cancellation rule** — when a task moves to `cancelled`:
1. Set `status: cancelled` + `completed` + `completed_during`.
2. Wrap the heading text in `~~`: `## ~~Task Title~~ {#task-id}`.
3. Append a `### Why cancelled` subsection in the prose body.
4. Section stays in the file as searchable history; never deleted.

**Feature → workflow hierarchy** — a `feature` task may declare subtasks
(workflows). The feature's prose body MUST list its subtasks as markdown
checkboxes: `- [x]` when the subtask's status is `done` or `functional`,
`- [ ]` otherwise. Checkbox state mirrors the metadata; both update
together on every status change. A feature can only reach `done` /
`functional` when all its subtasks have reached `done` / `functional`.

**Cross-references** use markdown links with relative path + anchor:
`[task-id](TODO.<component>.md#task-id)`.

---

### CHANGELOG.md

Repo-wide, dated, append-only record of feature-level completion
milestones. Lives at the repository root.

- One entry per feature that reached `done` or `functional`.
- Grouped by date.
- Each entry references the feature task (via cross-reference) and the
  workstream that closed it.
- Workstream-only changes that didn't close a clear feature (refactors,
  infra fixes) get a one-line entry referencing the squash.

**Operator gate** — at workflow end, when one or more features
transitioned to `done`/`functional` during the workstream, the agent MUST
ask the operator explicitly per feature whether to promote to
`CHANGELOG.md`. Not automatic. Phrasing pattern: "Feature `<id>` reached
`functional` this workstream — promote to CHANGELOG.md?". Operator can
defer individual features.

---

### Decisions files

Architectural and spec decisions live in `docs/decisions.md` (cross-cutting)
and `<component>/docs/decisions.md` (per-component), appended in
**chronological order** (oldest at top, newest at bottom).

**Reading order** — agents MUST read decisions **old to new** at session
start. Reading top-to-bottom in chronological order is what makes the
supersession rules below work.

**Supersession rule** — when a new decision contradicts an older one:
1. Find the superseded decision in its file.
2. Wrap its heading in `~~`: `## ~~Decision-NNN: <Title>~~`.
3. Append a `> Superseded by Decision-MMM ([link](#decision-mmm-...)).`
   line directly under the struck heading.
4. Leave the body intact (history is preserved; supersession is a marker).
5. Notify the operator in the chat turn introducing the superseding
   decision: "Decision-MMM supersedes Decision-NNN ('<old title>')."

**Idiosyncrasy detection** — when reading decisions old-to-new, if an
agent finds two decisions that conflict without a documented supersession
(e.g. Decision-X says "always do A", Decision-Y says "never do A",
neither references the other), warn the operator explicitly and ask
which is current before proceeding with work affected by either.

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
