- created: 2026-07-12
- created_by: fable-5
- completed: 2026-07-17
- completed_during: f/registry-file-set

## Blockers
- none

## Questions
- none

## Findings
- readme-sync trigger has fired (user-facing tool exists); no README/ARCHITECTURE/
  CHANGELOG/decisions in orchids yet; session rulings live only in chat + git log.
- Operator ruling (2026-07-16): README is mandatory and contains the WHY and the
  WHAT only; the HOW goes in ARCHITECTURE.md.
- Operator ruling (2026-07-16): owin.org was NEVER in the plans — it was invented
  by an agent session (commits f426a02/56bba34, 2026-07-12). install.txt header
  fixed; CNAME + index.html remain for the operator to delete.
- 2026-07-16: README.md and ARCHITECTURE.md written (why/what vs how split).
  Still missing: CHANGELOG, docs/decisions.md.
- Operator (2026-07-16): the GitHub `kauk` username/org is not yet available;
  waiting on it for the canonical repo list. Until then the interim homes are
  `serialseb/kauk` and `serialseb/orchids` — the explicit URLs in README.md,
  ARCHITECTURE.md, and Agent-installation.md are deliberate placeholders to
  swap when the `kauk/*` namespace lands.
- Operator (2026-07-16): the bootstrap contract is "install kauk/orchids" →
  the agent resolves the repo on GitHub and reads `Agent-installation.md`
  (where to go, what to install). install.txt renamed accordingly.
- Close provenance (2026-07-17): the original branch build was invalid — its
  anchor carried a fabricated `Base:` SHA (`4035d21ec2f3…`, a hallucinated
  expansion of the real `4035d21a2fe1…`; two attempts, 333864c then 95f41a6,
  both wrong) and it was built in the main working tree, not a worktree. The
  branch was rebuilt at close with the corrected trailer; all four work
  commits cherry-picked verbatim, author/committer dates preserved, trees
  byte-identical to old head b445dfa.
- index.html regenerated from Agent-installation.md at close (operator
  choice) so the still-served page carries the current contract; deleting
  CNAME + index.html remains reserved to the operator per the 2026-07-16
  owin.org ruling.

Result: done — registry file set landed; squash-merged to main at the close
of f/registry-file-set (tombstone: archive/registry-file-set).

## Proposal
Write the registry set: README (why + what only), ARCHITECTURE (the how, one page),
docs/decisions.md seeded with session rulings (.git-channel handover, .ai.toml
modes, fixed roles), CHANGELOG.

## Testing
readme-sync checklist passes; decisions greppable by #keyword.
