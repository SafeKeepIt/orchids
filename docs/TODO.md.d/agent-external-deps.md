- created: 2026-07-17
- created_by: opus-4.8

## Blockers
- Deliberately deferred by the operator (2026-07-17). In-package dependencies land
  first (`agents-first-class`); this is the generalisation and is not to be designed
  into that task.

## Questions
- What kinds of external dependency are in scope? Candidates, each a different problem:
  a skill from **another source** (`serialseb/kauk` ships one today, and every repo
  carries ≥2 sources); a **system tool** (`bw`, `gpg`, `pcscd` — the web-signup skill
  would need `bw`); a **runtime/service**.
- Declaration syntax: how does a dependency name something outside the package without
  assuming the other source is installed, or its version?
- What happens at install when an external dependency is absent — refuse, warn, or lay
  the agent and let it fail at use? A greyed-out row (the `agents-first-class` pattern)
  cannot express "you must go install this elsewhere first".
- Does this collide with `multi-source-namespacing`? Cross-source references need
  qualified ids, which that task already parks as unbuilt.

## Findings
- Operator ruling (2026-07-17): an agent's frontmatter dependency list "could be just a
  list of skills inside the package **or external dependencies** — but we'll put that in
  the future task to work on". So the *concept* is accepted; only the timing is deferred.
- The constraint on `agents-first-class`: do not design for external deps, but do not
  preclude them. A syntax that can only ever name in-package skills would have to be
  broken later.
- Relevant context, not a decision: `.ai.toml` already carries a sources dimension
  (`[sources."<owner>/<repo>"]`) and every repo carries ≥2 sources (kauk + orchids), so
  the multi-source world already exists — what is missing is qualified ids and collision
  rules. See `multi-source-namespacing`.

## Proposal
Design note only, when the operator picks it up. Nothing to build now.

## Testing
n/a — design artifact until scoped.
