- created: 2026-07-17
- created_by: opus-4.8

## Blockers
- None to start. The data can land while kauk still ignores it (unknown frontmatter
  keys are inert — kauk has no YAML reader at all), so orchids is not gated on kauk.

## Questions
- Ship order: land the whole DAG in one branch, or one child at a time? The terseness
  pass (`skill-terseness-pass`) touches all 26 files and will conflict with the
  rename/split work if run in parallel.

## Findings
- Spanning parent for the role-delivery programme decided 2026-07-17
  (Decision-002 mechanism, Decision-003 vocabulary). Read those first — this sidecar
  does not restate them.
- The problem being solved is measured, not assumed: 26 skills, 10,190 bytes of
  `description:` frontmatter loaded in every session of every repo. Under
  Decision-003, orchids itself would load `general` + `process/workflow` +
  `development` and drop the rest.
- The existing `role` field is inert. kauk `resolve_mode` (`bin/kauk:41-56`) uses it
  as an `.ai.toml` section-name lookup only; no `.ai.toml` in the fleet has a role
  section; all 26 skills link into every repo today. Verified against
  `.claude/skills/`.
- Division of labour is settled: orchids ships vocabulary + declarations + dependency
  edges; kauk owns the reader, the install-time picker, and the filter. Any engine
  work found during this programme belongs in serialseb/kauk, not here — and belongs
  on **kauk's board**, not tracked from this one.
- The kauk half is filed: `role-aware-delivery` on serialseb/kauk (`cli` /
  `cmd-install`, 2026-07-17). It carries the verified engine facts and the six
  implementation steps. It is the gate on this programme's Testing — the board edge
  cannot be expressed as a `⊘` token, since those resolve within one board only.
  Its two open questions (frontmatter syntax; stopgap vs 0.1.0) need answering on both
  boards at once, because orchids picks the syntax and kauk has to parse it in bash.

## Proposal
Four children, in dependency order:
1. `role-dag-frontmatter` — the frontmatter contract + declarations on all 26 skills.
2. `agents-first-class` — agents get identity, roles, and required-skill edges.
3. `skill-renames-and-splits` — `doing-skills` → `authoring-skills`; split `git-commit`.
4. `skill-terseness-pass` — quality pass over the corpus.

`authoring-skills` (the frontmatter contract's own spec) changes first within child 1,
or the other 25 have nothing to conform to.

## Testing
Per child. Roll-up exit: a scratch repo installing each role node in turn receives
exactly the declared subtree and nothing else — runnable only once kauk implements the
reader, so the orchids-side children test against a declaration lint instead.
