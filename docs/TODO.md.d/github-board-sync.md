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
- Ingestion automation shape: scheduled orchestrator session (schedule/cron)
  vs GitHub Actions — the single-writer rule favours the former; decide
  cadence and conflict handling with an interactive session holding the board.
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
  (same pattern as kauk sync); child sessions never touch GitHub. Ingestion
  may additionally run as a scheduled orchestrator-role job so the board
  converges without an interactive session.
- Pilot: orchids + kauk; the fleet follows via the package.

## Testing
An issue filed from the phone appears as a sidecar + board line after the next
sync; a board status change closes/updates its issue; the Project shows both
repos' active tasks with correct priority/readiness after push-back.
