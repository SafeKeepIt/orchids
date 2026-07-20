- created: 2026-07-20
- created_by: fable-5
- created_during: f/role-dag-frontmatter

## Blockers
- Lives in serialseb/kauk — no kauk edits from orchids; this entry routes the work.

## Questions
- None open — scope ruled by Decision-020.

## Findings
- orchids declares `roles:` on all 26 skills (f/role-dag-frontmatter); nothing
  validates them anywhere yet. Decision-020 places validation in kauk's reader —
  an orchids-side lint was ruled circular.

## Proposal
1. `kauk package validate .` stub returning 0, carrying a taxonomy TODO marker.
2. Real validation later, reader-side: every declared path resolves in the
   Decision-003 vocabulary (placement subsets allowed, no completeness check);
   every skill declares ≥1 role (explicit `general` counts).

## Testing
kauk-side; defined when the kauk task starts. orchids-side coverage was the
manual 26-skill diff against Decision-003 (run in f/role-dag-frontmatter, PASS).
