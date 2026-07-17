- created: 2026-07-17
- created_by: opus-4.8

## Blockers
- Depends on `role-dag-frontmatter` settling the role key + path syntax; agents reuse
  the same contract rather than inventing a second one.

## Questions
- Does the required-skill edge live in the agent's frontmatter (`requires: [groom]`) or
  in `manifest.conf`? Frontmatter matches Decision-002 ("authors declare"), but the
  manifest is what kauk parses today.
- What does kauk do when a selected role pulls in an agent whose required skill was
  excluded — install the skill anyway, or refuse the selection? A kauk ruling, but
  orchids should state the intent.
- Should agents keep their own delivery type (`agent <name> <role>`) or become a skill
  variant? Affects how much of kauk's `lay_source` changes.

## Findings
- Agents are `link` lines today — `link agents/architect.md .claude/agents/architect.md`
  — which the manifest header documents as "everyone gets it". All 5 agents install
  unconditionally into every repo, with no role and no opt-out. Skills at least have a
  (dead) role field; agents have nothing.
- Agent frontmatter carries only `name`, `description`, `model`. No role, no deps.
- Real dependency edges exist and cannot currently be stated: the workflow needs the
  groomer; the architect needs `workflow` + `workflow-complete` + `handover`; the
  housekeeper needs `workflow-complete` + `readme-sync`. These are assumptions today.
- kauk's `lay_source` dispatch (`bin/kauk:114-140`) is a bare `read -r t a b _rest`
  case statement; an unknown type warns and skips. A new `agent` line type is a small,
  additive change — but it is kauk's change, not orchids'.

## Proposal
1. Declare roles on all 5 agents using the contract from `role-dag-frontmatter`.
2. Declare required-skill edges per agent.
3. Keep the `link` lines working until kauk ships the reader, so nothing regresses.

The `agent` manifest line type and the dependency resolution are **kauk's work and live
on kauk's board** — `role-aware-delivery` (`cli` / `cmd-install`), filed 2026-07-17.
Do not re-specify them here; state intent and let that task own the engine.

## Testing
Declaration lint: every agent declares ≥1 role; every `requires:` id resolves to a real
skill in the package. End-to-end (a role selection installing an agent plus exactly its
required skills) is kauk-side and cannot be run here — report it as untested, not as
passing.
