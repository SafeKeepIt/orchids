- created: 2026-07-12
- created_by: fable-5

## Blockers
- GATES ANY PUSH ANYWHERE (operator, 2026-07-12: "needs a lot of cleanup").

## Questions
- Split shape: public process repo + private forensic/infra skill source?
- Keep owin.org pointing at the public part only?

## Findings
- Forensic skills carry live-incident detail (themis, clean-host doctrine, attacker
  context, exhibit numbers); agents/docs reference operator infrastructure; canonical
  paths embed /home/sudoku. Repo history is young — a clean re-init is cheap if
  scrubbing history beats rewriting it.

## Proposal
Sensitive-content sweep (files + history) per AGENTS.shared.md; propose the
public/private split; scrub or re-init; only then the publish ceremony (gh repo,
Pages, DNS).

## Testing
Independent sweep of the candidate-public tree finds nothing sensitive; install flow
works from the public URL end-to-end on a scratch repo.
