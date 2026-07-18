- created: 2026-07-18
- created_by: fable-5
- created_during: interactive

## Blockers
- None.

## Questions
- Should the kauk install id move from `serialseb/orchids` (and eventually
  `serialseb/kauk`) to `kaukea/*`? The id names the vendored clone path
  (`.ai/repositories/<owner>/<repo>`) in every consuming repo, so a change is a
  managed-artifact migration (dated migrations entry + kauk sync handling), not
  a find-and-replace.

## Findings
- The repo now lives at github.com/kaukea/orchids (Decision-012 + transfer,
  2026-07-18). Consuming repos on this Pi install via local-path origins, so
  nothing is broken today; GitHub redirects cover the old SafeKeepIt URL.

## Proposal
Defer until the org name is final (dormant-username requests for kauk/kaukai
are pending — an org rename would change the id again). Then migrate ids and
clone paths in one dated migration.
