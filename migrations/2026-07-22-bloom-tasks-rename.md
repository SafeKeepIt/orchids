# 2026-07-22 — `ripen-tasks` skill renamed `bloom-tasks`; `ripener` agent renamed `bloomer`

The board-readiness skill and its prep-only agent are renamed (Decision-050: the
ripen word family is retired from the vocabulary; tasks bloom, the agent is the
bloomer). Consuming repos drop any stale laydown of the old names so only
`bloom-tasks` and `bloomer` (placed fresh by `kauk sync`) remain. Link-mode
installs are already pruned by `kauk sync` (the targets are gone after the
rename); this migration cleans stale symlinks for older kauk versions and flags
the copy/local case for judgement — a real directory or file may carry local
edits and is never clobbered.

## Detect → convert

```sh
# Remove old-name laydowns ONLY when they are symlinks whose target is gone
# (dangling after the package rename). Real files/directories (copy/local mode)
# are left untouched for the judgement step below.
for d in ".claude/skills/ripen-tasks" ".claude/agents/ripener.md"; do
  if [ -L "$d" ] && [ ! -e "$d" ]; then rm "$d"; fi
done
true
```

## Then: reconcile a copy/local install (judgement)

If `.claude/skills/ripen-tasks` still exists as a real directory, or
`.claude/agents/ripener.md` as a real file (copy or `local` mode in `.ai.toml`),
they are pre-rename local variants. Move any local edits into
`.claude/skills/bloom-tasks` / `.claude/agents/bloomer.md` (placed by
`kauk sync`), then remove the old paths. Update any repo-local reference to the
old skill or agent name, including `.claude/state/last-ripen.sha` →
`.claude/state/last-bloom.sha` if present.

## Verify

Neither `.claude/skills/ripen-tasks` nor `.claude/agents/ripener.md` remains (no
dangling symlink and, after reconciliation, no real file); the readiness skill
is present as `.claude/skills/bloom-tasks` and the prep agent as
`.claude/agents/bloomer.md`.
