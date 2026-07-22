- created: 2026-07-22
- created_by: gh-ingest
- created_during: interactive

## Blockers
- None known yet.

## Questions
- Ingested from GitHub issue #93 — needs triage: type, component,
  urgency, scope.

## Findings
- Filed on GitHub (https://github.com/kaukea/orchids/issues/93); original body preserved below.

#roles #frontmatter #role-delivery #skills #agents #kauk #taxonomy

Three rulings, closing `role-dag-frontmatter`'s questions:

- **Key + syntax:** `roles:` is a list of slash-separated full paths —
  `roles: [development/tofu, infrastructure/tofu]`. Rejected: bare node ids
  (ancestry invisible at the declaration site), nested YAML and `role:` + `parent:`
  pairs (tree edges copied into every declarer).
- **Paths are placements.** A declared path is a deliberate placement, and a
  multi-parent node may be placed under a subset of its parents —
  `roles: [development/tofu]` alone is valid, making per-route delivery expressible.
  Lint verifies each declared path exists in the vocabulary; an incomplete set is
  intent, not an error class.
- **`general` is explicit** (`roles: [general]`). A missing `roles:` key is a lint
  error — "forgot to declare" is never readable as "deliberately general".

Context, not ruling: the vocabulary stays declared in exactly one place
(Decision-002/003). The sidecar's "one round with kauk before committing" was waived
by ruling directly; kauk's reader implements this contract as written.
