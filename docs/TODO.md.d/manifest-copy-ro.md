- created: 2026-07-18
- created_by: fable-5
- created_during: interactive

## Blockers
- None.

## Questions
- Attribute syntax placement: trailing `[copy,ro]` on any manifest entry line
  — confirm it applies to `link` (and `skill`?) entries, and how it interacts
  with per-repo .ai.toml delivery modes (author-specified attribute vs
  consumer-tuned mode precedence).
- Does sync re-copy an `ro` file when the package source changes? (Intended
  reading: yes — ro guards against CONSUMER edits, not package updates; that
  is what distinguishes it from `template`.)

## Findings
- Operator spec (2026-07-18): extend the kauk manifest with per-entry
  attributes `[copy,ro]`, matching other tools' featuresets (chezmoi-style
  attributes). `copy` lays a real file instead of a symlink; `ro` chmods it
  read-only AND excludes it from sync take-up of consumer-side changes
  (which sync doesn't do today anyway — the attribute makes it a contract).
- Killer use case: `.github/workflows/` shims. `template` never propagates
  updates; a `link` is a dangling symlink on GitHub. `copy,ro` gives a real
  committed file Actions will run, that consumers can't drift, and that sync
  keeps current. Pairs with the reusable-workflow pattern (shim `uses:` the
  central workflow in the package repo) — see github-board-sync.

## Proposal
Upstream kauk change: manifest parser accepts a trailing `[attr,...]` list;
lay_source honours `copy` (copy_one instead of link_one) and `ro`
(chmod a-w after laying; sync refreshes from source but never absorbs or
pushes back consumer edits). Carried on the orchids board per the
upstream-kauk precedent.

## Testing
A manifest line `link x .github/workflows/x.yml [copy,ro]` lays a real
read-only file; editing it locally is blocked; changing the source and
running kauk sync refreshes it; git status in the consumer stays clean of
sync-side noise.
