- created: 2026-07-18
- created_by: fable-5
- created_during: interactive

## Blockers
- None.

## Questions
- ~~Precedence between the file's attributes and consumer .ai.toml~~ —
  RESOLVED (operator, 2026-07-18): the package is always right. Deferred
  extension (much later, explicitly out of scope now): a consumer with push
  permission on the package source may change the attribute AT THE SOURCE
  and that is respected — write access to the package is the override, not
  a local setting.
- Does sync re-copy an `ro` file when the package source changes? (Intended
  reading: yes — ro guards against CONSUMER edits, not package updates; that
  is what distinguishes it from `template`.)
- Non-markdown deliveries (e.g. a workflow .yml) cannot carry markdown
  frontmatter — comment-based marker (`# kauk: copy,ro`), a sidecar
  attribute file, or manifest fallback for those?

## Findings
- Operator spec (2026-07-18, corrected): the attributes live in the
  delivered FILE'S OWN FRONTMATTER, not on manifest.conf lines, and apply
  to file deliveries (link-type), not skills. Precedent: skill frontmatter
  already carries non-schema keys under `metadata:` (`tags:`, `share:`) —
  the harness tolerates them; delivery attributes extend the same channel
  (chezmoi-style attributes, matching other tools' featuresets). `copy`
  lays a real file instead of a symlink; `ro` chmods it read-only AND
  contracts that sync never takes up consumer-side changes (which it
  doesn't do today anyway — the attribute makes it explicit).
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
