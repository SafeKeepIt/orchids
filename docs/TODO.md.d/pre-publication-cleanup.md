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
- 2026-07-14 (tool-split-to-kauk): the publishable surface of THIS repo no longer
  includes code — the tool lives in serialseb/kauk. The public/private split question
  above now applies to the skill/data set only. NOTE: an EMPTY public
  github.com/serialseb/kauk was created by a failed cloud run on 2026-07-14; nothing
  was pushed, but the gate applies to any future push there too (kauk repo content
  references operator infrastructure).

## Proposal
Sensitive-content sweep (files + history) per AGENTS.shared.md; propose the
public/private split; scrub or re-init; only then the publish ceremony (gh repo,
Pages, DNS).

## Testing
Independent sweep of the candidate-public tree finds nothing sensitive; install flow
works from the public URL end-to-end on a scratch repo.
