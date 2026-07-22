# Retire the ripen word family: rename the skill, the agent, and the verb

- created: 2026-07-20
- created_by: Sebastien Lambla
- completed: 2026-07-22
- completed_during: orchestrator session

## Blockers

- None.

## Questions

- ~~Replacement word for the original (groom) family?~~ RULED (operator, 2026-07-20,
  Decision-026): **ripen/ripener** — executed 2026-07-20 (migration
  `2026-07-20-ripen-tasks-rename.md`).
- ~~Replacement word for the ripen family, once that too was marked for
  retirement?~~ RULED (operator, 2026-07-22, Decision-050): **bloom/bloomer** —
  tasks bloom until pickable; the agent is the bloomer.
- ~~Skill name?~~ Bare verbs break the corpus's verb-object convention
  (`read-agents`, `write-to-s3`, `authoring-skills`) — operator flagged the
  convention on the first rename. `bloom-tasks` follows it; agents are role
  nouns, so `bloomer` stands.

## Findings

- Operator (2026-07-20): the original word family is FORBIDDEN — it relates to bad
  people in other contexts. Applies to all output, not only these two artifacts.
  The ripen family was subsequently marked for retirement as well; the operator
  chose bloom on 2026-07-22.
- Footprint (second rename, as executed): `skills/ripen-tasks/` → `skills/bloom-tasks/`,
  `agents/ripener.md` → `agents/bloomer.md`, the verb across `agents/orchestrator.md`,
  `skills/orchestrator/SKILL.md`, `README.md`, `AGENTS.files.md`, `ARCHITECTURE.md`,
  `tools/board_stale.py`, `tools/board_lint.py`, and open-task sidecar prose.
  Skill and agent are MANAGED ARTIFACTS — the rename ships with a dated migration
  (§Migrations), like the two precedents.

## Proposal

Rename the skill and agent, sweep the verb across the corpus, update README
references, ship the migration. One sweep, one branch.

## Testing

Corpus grep for the old family returns only the migration files and history; a
consuming repo syncs cleanly with the renamed artifacts; the readiness pipeline
prose reads naturally with the new word.

### Resolution (2026-07-22)

Executed directly on main (workflow component, Decision-065) on the operator's
"done now" order, folded into Decision-050 together with the new mandatory
handoff bloom round: `bloom-tasks`/`bloomer` landed with migration
`2026-07-22-bloom-tasks-rename.md`, the verb swept corpus-wide (35 files;
done/cancelled sidecars, decisions, CHANGELOG and the 2026-07-20 migration left
as history), commit template now `🌸 bloom: <id> → <stage>`, state file renamed
`last-bloom.sha`. Test: corpus grep clean outside history; `kauk sync` run;
prose reads naturally.
