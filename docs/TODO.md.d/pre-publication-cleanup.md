- created: 2026-07-12
- created_by: fable-5

## Blockers
- GATES ANY PUSH ANYWHERE (operator, 2026-07-12: "needs a lot of cleanup").

## Questions
- Split shape: public process repo + private forensic/infra skill source?
- Keep owin.org pointing at the public part only?

## Findings
- **2026-07-18 EXPOSURE (operator ruling: treat as leak).** Both repos were made
  public and pushed with full history — orchids ~19:55–22:45 CEST (renamed
  aihelp), kauk ~20:20–22:45 — in breach of this task's push gate, which was
  not consulted. World-readable during the window: every forensic/infra skill,
  boards, decisions, /home/sudoku paths; plus 28 board issues (still present,
  now private with the repos). Orchidarium project was private throughout.
  Consequence: any re-publicizing REQUIRES the history scrub below first; the
  public/private split decides what a scrubbed public surface even contains.
- Forensic skills carry live-incident detail (themis, clean-host doctrine, attacker
  context, exhibit numbers); agents/docs reference operator infrastructure; canonical
  paths embed /home/sudoku. Repo history is young — a clean re-init is cheap if
  scrubbing history beats rewriting it.
- 2026-07-14 (tool-split-to-kauk): the publishable surface of THIS repo no longer
  includes code — the tool lives in serialseb/kauk. The public/private split question
  above now applies to the skill/data set only. NOTE: an EMPTY public
  github.com/serialseb/kauk was created by a failed cloud run on 2026-07-14; nothing
  was pushed, but the gate applies to any future push there too (kauk repo content
  references operator infrastructure).

- 2026-07-17: operator flagged `write-to-s3` as likely carrying private information
  that must not be published — named specifically, ahead of any sweep. Treat it as a
  known hit, not a candidate. Its role placement is parked on this task's outcome
  (Decision-003 leaves it provisionally at `security/forensics`).
- 2026-07-17: the role DAG (Decision-002/003) gives this task a mechanism it did not
  have. `security/forensics` is a named subtree, so the public/private boundary can be
  expressed as a role selection rather than a bespoke file list — IF the boundary turns
  out to follow the taxonomy. Worth testing that hypothesis early; do not assume it.

## Proposal
Sensitive-content sweep (files + history) per AGENTS.shared.md; propose the
public/private split; scrub or re-init; only then the publish ceremony (gh repo,
Pages, DNS).

## Testing
Independent sweep of the candidate-public tree finds nothing sensitive; install flow
works from the public URL end-to-end on a scratch repo.
