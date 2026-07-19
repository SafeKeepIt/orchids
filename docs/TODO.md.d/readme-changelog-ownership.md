- created: 2026-07-19
- created_by: fable-5

## Blockers

_None._

## Questions

- Does the orchestrator write these at close from the feature's sidecar result, or does the
  housekeeper write them under orchestrator instruction? (The housekeeper currently verifies
  rather than authors.)

## Findings

- The single-writer rule today names only the board and `docs/decisions.md` as orchestrator
  owned — "child sessions do not write those directly." README and CHANGELOG are left to the
  feature branch, with the architect authoring and the housekeeper verifying.
- **That does not work, evidenced 2026-07-19.** The message-bus architect wrote CHANGELOG
  entries by imitating existing ones without ever opening `AGENTS.files.md`, and edited the
  README without loading `readme-sync` — the skill its own close gate names. Both were
  specified; both were skipped; the output looked plausible.
- These are repo-level integration artifacts, the same category as the board and decisions: a
  feature-scoped agent sees one feature and writes them from that vantage, which is exactly
  why the board was made orchestrator-owned in the first place.

## Proposal

Move README.md and CHANGELOG.md to the orchestrator, alongside the board and decisions.
Architects stop touching them; they report what changed in their sidecar result and the
orchestrator writes the repo-level record at close.

## Testing

A feature closes without its architect having edited either file, and both are correct
afterwards.
