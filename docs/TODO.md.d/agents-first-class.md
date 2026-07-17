- created: 2026-07-17
- created_by: opus-4.8

## Blockers
- Depends on `role-dag-frontmatter` settling the role key + path syntax; agents reuse
  the same contract rather than inventing a second one.

## Questions
- Dependency list syntax — reuse whatever `role-dag-frontmatter` picks for roles, or a
  separate key? (`requires: [groom, handover]` alongside `roles: [...]` is the obvious
  shape, but the two tasks must agree once, not twice.)
- Do agents depend on **other agents**? The real graph has them: the orchestrator hands
  to `architect` / `housekeeper` / `groomer`; the architect dispatches `builder`. Deploy
  `architect` without `builder` and it is broken, and nothing declares that today. The
  operator ruling covers agent→skill; agent→agent is unstated. Confirm before building.

## Findings
Operator rulings, 2026-07-17 — these close what were the three open questions here:
- **The dependency list lives in the agent's OWN frontmatter.** A list of skills shipped
  inside the package. Consistent with Decision-002: authors declare, because they know.
- **External dependencies are deferred**, deliberately — a dependency could one day be
  outside the package (another source's skill, a system tool). Not now; filed as
  `agent-external-deps`. Do not design for it here, only avoid precluding it.
- **The package layout gains an `agents/` folder, symmetric with `skills/`**, linked
  into place from its own location exactly as skills are. Agents are not a skill
  variant; they are a peer artifact with a peer folder.
- **An agent may require MULTIPLE skills that ship with it, and that changes how
  choosing skills works** — this is the consequence that drives the install flow, see
  below.

Background (unchanged):
- Agents are `link` lines today — `link agents/architect.md .claude/agents/architect.md`
  — which the manifest header documents as "everyone gets it". All 5 agents install
  unconditionally into every repo, with no role and no opt-out. Skills at least have a
  (dead) role field; agents have nothing.
- Agent frontmatter carries only `name`, `description`, `model`. No roles, no deps.
- Real dependency edges exist and cannot currently be stated: the workflow needs the
  groomer; the architect needs `workflow` + `workflow-complete` + `handover`; the
  housekeeper needs `workflow-complete` + `readme-sync`.

## Proposal
1. Declare roles on all 5 agents using the contract from `role-dag-frontmatter`.
2. Declare each agent's required-skill list in its own frontmatter.
3. Keep the `link` lines working until kauk ships the reader, so nothing regresses.

**Two-page install selection (operator, 2026-07-17)** — the flow, which orchids
specifies and kauk implements:
- **Page 1: choose agents.**
- **Page 2: choose skills** — the skills required by the agents chosen on page 1 appear
  **greyed out**: visible, already selected, not deselectable.

Greyed-out rather than hidden is the point. The operator sees exactly what their agent
choice pulled in and why it is not theirs to uncheck — the requirement is legible
instead of silently applied. A hidden pre-selection would leave them wondering later why
a skill they never picked is in their repo.

This is also why agents come first: an agent is the thing an operator actually wants,
and its skills follow from it. It dissolves the "what if a required skill was excluded?"
question — the flow makes it unaskable rather than answering it.

The `agent` manifest type, the `agents/` folder handling, the dependency resolution and
the two-page picker are **kauk's work, on kauk's board** — `agent-deployment` (`cli` /
`cli-core`), filed 2026-07-17. State intent here; do not re-specify the engine.

## Testing
Declaration lint: every agent declares ≥1 role and a resolvable `requires:` list — every
id names a real skill in the package. End-to-end (page 1 → page 2 → exactly the right
set laid) is kauk-side and cannot run here; report it untested rather than implied.
