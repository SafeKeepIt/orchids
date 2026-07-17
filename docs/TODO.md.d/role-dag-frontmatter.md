- created: 2026-07-17
- created_by: opus-4.8

## Blockers
- None. Declarations are inert until kauk reads them; landing them early is safe.

## Questions
- None open — ruled 2026-07-17 (Findings, Decision-005).

## Findings
- Frontmatter is currently inconsistent and has never been machine-read: all 26 carry
  `name` + `description`; only 17 have `metadata`; 4 `share`; 4 `compatibility`;
  3 `tracked`. kauk touches `SKILL.md` at 5 places, all byte-level (`cmp -s`, `-e`,
  `cp`) — there is no YAML reader. Whatever key we add is the first frontmatter field
  that does anything.
- Existing `metadata.tags` are grep-bait keyword soup, not a taxonomy, and are consumed
  by nothing. `doing-skills` ships the literal placeholder
  `tags: [ <grep-able trigger words> ]`. Do not overload `tags` for roles.
- `skills/doing-skills/SKILL.md` defines the frontmatter contract the other 25 follow,
  so it is the keystone — it changes first or there is nothing to conform to. (It is
  also being renamed; see `skill-renames-and-splits`.)
- The node list is fixed by Decision-003. This task applies it; it does not relitigate it.

Operator rulings, 2026-07-17 (Decision-005) — close both questions; ruled directly,
the "one round with kauk first" waived (kauk's reader implements what is ruled here):
- **`roles:` is a list of slash-separated full paths** —
  `roles: [development/tofu, infrastructure/tofu]`. Chosen over bare node ids and
  over nested YAML / `role:` + `parent:` pairs.
- **Paths are placements.** Each declared path is a deliberate placement; an author
  MAY place a multi-parent node under a subset of its parents
  (`roles: [development/tofu]` alone is valid). Lint checks each declared path exists
  in the vocabulary — never completeness. Per-route delivery is expressible.
- **`general` is explicit** — `roles: [general]`; a missing `roles:` key is a lint
  error, so "forgot" is never readable as "deliberately general".

## Proposal
1. Amend the frontmatter contract in `authoring-skills` (née `doing-skills`) with the
   ruled contract: `roles:` slash-path list, placement semantics, explicit `general`
   (Decision-005), and the DAG rule (multi-parent allowed).
2. Declare roles on all 26 skills per Decision-003.
3. Add a lint (extend `tools/board_lint.py` or a sibling) asserting: every skill
   declares ≥1 role (explicit `general` counts); every declared path resolves to an
   existing path in the vocabulary (placement subsets allowed — no completeness
   check); the vocabulary itself is declared in exactly one place.
4. Leave `manifest.conf`'s `role` field alone in this task — retiring it is kauk-facing
   and needs the reader to exist first.

## Testing
Lint run over the corpus: 26/26 skills declare a resolvable role path; a deliberately
bad path fails the lint, and so does a skill with no `roles:` key. Manual read-through of the diff against the Decision-003 tree.
Delivery itself cannot be tested until kauk implements the reader — say so, do not
imply otherwise.
