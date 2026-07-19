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
- **Therefore a repo cannot have its own hooks.** Adding a TV-specific hook to seb.tv means
  editing the shared file, which imposes it on kauk, signmc, TitanShield and everything else.
  There is no per-repo surface in use — hooks that should be local end up in one global pool.
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
