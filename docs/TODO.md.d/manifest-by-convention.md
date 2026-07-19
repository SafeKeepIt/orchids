- created: 2026-07-19
- created_by: fable-5
- created_during: f/status-channel

## Blockers

_None._

## Questions

- Does this land before or after the real kauk CLI? `manifest.conf` is parsed by the
  `kauk-sync` stopgap, which is documented as dying when the real CLI ships — so the fix may
  belong in that CLI's design rather than in the stopgap. The lint below is worth doing
  either way because it is a few lines.

## Findings

- **The manifest is a hand-typed index of files the package already contains.** kauk reads it
  with `grep -Ev '^[[:space:]]*(#|$)' manifest.conf` — no derivation, no validation, nothing
  reconciling it against the tree.
- **Nothing catches a missing entry, and the failure is silent.** On 2026-07-19 four files
  (`agents/bus.md`, `hooks/bus-init.sh`, `hooks/bus-end.sh`, `tools/bus.py`) were committed,
  reviewed and tested, and distributed to nobody — because four lines were missing from this
  file. The mechanism was reported as working while it had never run in any session.
- **It is not an allowlist for shipping.** The consumer gets the WHOLE repo: the clone at
  `.ai/repositories/<owner>/<repo>/` contains `docs/`, `migrations/`, the board and
  `ARCHITECTURE.md` regardless. The manifest only picks which files are symlinked into
  `.claude/` — so nothing is being withheld from anyone and the "we must declare what ships"
  justification does not hold.
- **Most entries restate their own path.** `link agents/x.md .claude/agents/x.md` is the
  source path with a prefix swapped. Four directory conventions cover every one of them:
  `agents/*.md`, `hooks/*.sh`, `tools/*`, `skills/<name>/`.
- **What is genuinely not derivable is small:** the `link` vs `template` distinction (one
  tracks upstream, the other is copied once at install and thereafter owned by the project) —
  which a `templates/` directory would express — and `option` lines, which describe the
  package rather than any file. Per-skill roles are already migrating to frontmatter under
  [[role-dag-frontmatter]].

## Proposal

Derive distribution from the tree instead of authoring it. Directory conventions replace the
per-file `link` and `skill` lines; whatever cannot be derived (delivery semantics, package
options) moves somewhere that is not a parallel copy of the directory listing.

**Do the cheap half first regardless of the above:** a lint that compares the payload
directories against the manifest and fails on anything present in the tree but undeclared.
That alone converts the silent failure into a loud one, and would have caught the 19 July bug
at commit time.

## Testing

A file added to a payload directory and not declared must cause a visible failure — and once
derivation lands, must be distributed without anyone editing an index.
