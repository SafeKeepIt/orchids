- created: 2026-07-12
- created_by: fable-5

## Blockers
- dot.ai territory — design only while the stopgap lives.

## Questions
- Conflict rules when two sources ship the same skill name?

## Findings
- .ai/repositories/<owner>/<repo>/ already namespaces checkouts; manifest and
  .ai.toml assume ONE source. Operator: "imagine myorchestrator and OhMyCode both
  installed — a nightmare" — "we can namespace later".
- 2026-07-14 (tool-split-to-kauk): .ai.toml now has a sources dimension
  (`[sources."<owner>/<repo>"]` tables) and every repo carries ≥2 sources (kauk +
  orchids); per-source manifests exist. Skill-name collision handling and qualified
  ids remain unbuilt — still parked.

## Proposal
Design note only: per-source manifests, qualified skill ids on collision, .ai.toml
gains a source dimension.

## Testing
n/a — design artifact.
