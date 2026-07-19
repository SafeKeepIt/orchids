- created: 2026-07-19
- created_by: fable-5

## Blockers

_None._

## Questions

- Should repo-specific hooks live in `.claude/settings.local.json` (which exists and is not
  linked), leaving the package's `settings.json` for package hooks only? That may already be
  the answer and simply be undocumented and unused.
- Do hooks want declaring per-package the way manifest entries are, and composing at sync
  time — or is a local-overrides file enough?

## Findings

- **`settings.json` is delivered as a `link`** (`link settings.json .claude/settings.json`),
  so every consuming repo SYMLINKS one shared file. Verified: seb.tv's `.claude/settings.json`
  points into its orchids clone.
- **Correction (verified 2026-07-19): a repo CAN opt out, but cannot COMPOSE.** kauk refuses
  to lay a link over a real file — `BLOCKED <link> (real file present — run 'kauk install' to
  migrate, or mark it local/copy in .ai.toml)` — so `.ai.toml` delivery modes are a designed
  per-repo escape hatch. What does not exist is a MERGE: a repo takes the package's settings
  wholesale, or owns its own and thereafter stops receiving package updates. Adding one
  TV-specific hook to seb.tv today means either imposing it on every other repo or forking
  the whole file.
- **Nothing is silently overwritten.** kauk BLOCKS on a real file and reports; `copy_one` is
  explicitly "never overwrite" and reports DRIFT instead. An earlier worry that installs may
  have clobbered pre-existing settings is unfounded — verified in the kauk source.
- **Claude Code does read a symlinked `settings.json`** — proven empirically, not assumed:
  the `UserPromptSubmit` migration and ingestion hooks and the `Stop` close hook all fired
  repeatedly through 19 July from seb.tv, whose `.claude/settings.json` is a symlink into its
  orchids clone.
- **Hook entries carry no provenance.** Each is an anonymous shell string inside a shared
  array. Nothing records which package, feature or session added it, so nothing can remove it,
  audit it, or tell a stale entry from a live one. The `hooks` object is append-only by
  construction.
- **The wrapper is copy-pasted per entry.** Every hook is
  `root="$(git rev-parse --show-toplevel)"; [ -x "$root/.claude/hooks/X" ] && "$root/.claude/hooks/X"; exit 0`,
  restating its own path — the same redundancy as the manifest's `link` lines.
- **Concurrent edits collide.** On 2026-07-19 two agents appended blocks to this file from two
  branches within an hour (a `UserPromptSubmit` pair and a `SessionStart` block); one of those
  edits used a substring duplicate-check written on the spot. JSON merges badly and there is
  no composition step to make it safe.
- `.claude/settings.local.json` exists in orchids and is NOT linked, so a per-repo channel is
  already available and simply unused.

## Proposal

Sort out where hooks live and who owns each one: a per-repo surface for repo-specific hooks,
provenance for package-supplied ones so they can be removed as well as added, and composition
instead of hand-editing a shared blob.

Same class as [[manifest-by-convention]]: a hand-edited shared config with no ownership and
nothing reconciling it. Worth solving with the same answer rather than a second bespoke one.

## Testing

A repo can add a hook that affects only itself; a package hook can be removed by removing the
package; and two features touching hooks in parallel do not conflict.
