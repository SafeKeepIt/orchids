- created: 2026-07-18
- created_by: fable-5
- created_during: interactive

## Blockers
- None.

## Questions
- Project field mapping: which board badge fields become Project custom fields
  (status/urgency/readiness/component/repo), and which saved views (master
  by-priority, by-repo, roadmap)?
- Cross-repo dependency representation: native sub-issues / dependency links
  vs a Project field mirroring `blocked_by` — verify what GitHub offers at
  build time.
- Claude GitHub App auth: API key vs subscription OAuth token, and secret
  distribution across the three owners (serialseb, SafeKeepIt, kaukea) —
  org secrets don't span owners.
- Injection/actor gating: on public repos anyone can file issues; the
  workflow must run the orchestrator only for the operator's own
  issues/comments (actor allowlist), never on third-party text.
- Workflow-file delivery: RESOLVED — a manifest `template` entry
  (`template templates/board-sync.yml .github/workflows/board-sync.yml`);
  it must be template, not link: a symlink would target the gitignored
  .ai/ clone and Actions only executes real files. Remaining: pushes
  touching workflow files need the workflows permission, and template
  files are project-owned, so template changes don't propagate on sync —
  acceptable for a stable trigger shim that delegates logic to the agent.
- Race with a live local session on main: cloud orchestrator pushes intake
  commits; local sessions already pull at start — define retry/ff-only
  behaviour on push rejection.
- Project naming and location (user-level project on serialseb).

## Findings
- Operator problem (2026-07-18): ~15 concurrent projects, some interdependent;
  no cross-project review of pending work and priorities. Console UI can't
  carry it; GitHub Projects v2 chosen as the view.
- A USER-level Project aggregates issues from repos across owners
  (serialseb, SafeKeepIt, kaukea) — org-level would not span them.
- The board badge already reserves a `gh#` column; issues follow each repo's
  visibility, so the board sanitization rule applies verbatim to issue bodies.

## Proposal
Operator rulings (2026-07-18):
- Files canonical; GitHub is the view. FULL ingestion at sync: GitHub-born
  issues become sidecars, field edits become board updates, comments land in
  the sidecar; then files rule until push-back.
- Issues for ACTIVE tasks only (todo/doing/blocked/paused; closed on
  done/cancelled). Issue body = sanitized summary + open questions; the
  sidecar stays the full record.
- Sync is the ORCHESTRATOR'S job only — pull at session start, push at close
  (same pattern as kauk sync); child sessions never touch GitHub.
- Ingestion is EVENT-DRIVEN over GitHub, not polled (operator, 2026-07-18):
  a GitHub Actions workflow in each repo receives issue/Project events and
  runs the Claude GitHub integration AS THAT REPO'S ORCHESTRATOR — the
  checkout carries the vendored orchids package, so the role, skills, and
  board rules are in place; it ingests the change into sidecar/board and
  commits to main. Local sessions stay for real work; the cloud orchestrator
  only triages board events. Works with the Pi off; no idle cron runs.
- Pilot: orchids + kauk; the fleet follows via the package.

## Testing
An issue filed from the phone appears as a sidecar + board line after the next
sync; a board status change closes/updates its issue; the Project shows both
repos' active tasks with correct priority/readiness after push-back.
