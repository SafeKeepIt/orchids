- created: 2026-07-14
- created_by: fable-5
- created_during: f/data-only-split

## Blockers

_None — executed 2026-07-14._

## Questions

_None open here; the install-UX question (plugin?) lives on the kauk board
(`kauk-sync-stopgap`)._

## Findings

- The tool (`bin/orchids`) moved to `serialseb/kauk` as `bin/kauk-sync`
  (kauk Decision-007/008). orchids is now DATA-ONLY: it exposes its files and their
  grouping in `manifest.conf` v2 typed lines (`skill`/`link`/`template`/`prefix`) —
  the engine hardcodes no layout.
- `skill-sync` is retired; its content lives on as the `kauk` skill, shipped by the
  kauk package itself (pull-only). `templates/CLAUDE.md` now holds the exact prefix
  block the engine lays (was duplicated as a heredoc in the old script).
- Consumers keep their `.ai/repositories/serialseb/orchids` clone path — migration
  only adds the vendored tool clone and `.ai.toml` `[sources]` tables.
- install.txt/index.html (owin.org) now bootstrap kauk first, then
  `kauk-sync install serialseb/orchids`.

## Proposal

Done: manifest v2, tool + skill-sync removal, prose repointing (doing-skills,
workflow, history-rewrite, read-agents), install page rewrite. The "orchids is a
stopgap, dies when dot.ai returns" framing now applies to `kauk-sync` (the stopgap
code) — orchids-the-package persists as the fleet's skill source.

## Testing

Fresh-repo simulation of the new install page; re-sync of the three consumers with
zero broken links; consumer→canonical round-trip edit; pull-only guard on the kauk
clone.
