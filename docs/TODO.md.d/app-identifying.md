- created: 2026-07-21
- created_by: fable-5
- created_during: f/cloud-architect
- completed: 2026-07-21
- completed_during: f/app-identifying

## Blockers

- None.

## Questions

- ~~App name?~~ RULED (operator, 2026-07-21): **callabloom** (`callabloom[bot]`),
  kaukea-owned, App ID 4354752. Supersedes the earlier "Kaukai" ruling — the app is the
  fleet's mixed-responsibility cloud bot, not a kauk-specific thing; and "Kaukai" / "calla"
  / "tigerlily" and their simple variants all collide with existing GitHub logins.
  "callabloom" (Calla + bloom, the Wonderland talking-flower theme) was free.
- ~~Where do the mint credentials live?~~ RULED (operator, 2026-07-21): kaukea ORG secrets
  `CALLABLOOM_APP_ID` + `CALLABLOOM_PRIVATE_KEY` (visibility ALL). One mint point; the
  consuming-repo inherit rides the deferred rollout.

## Findings

- The app is the CENTRALISED bot identity for the cloud hops: every GitHub action (comment,
  commit, PR, push, merge) is `callabloom[bot]` — never the operator, never the anonymous
  `github-actions`. That is the whole point ("pretending to be me is very poor").
- The original close-spine premise was OVERTURNED live (operator + `gh api`): ruleset
  19333120 no longer exists (deleted, not disabled); org-level rulesets need a GitHub Team
  plan (kaukea is Free); the only live rule is a minimal "Baseline" ruleset. So the
  branch-protection / bypass-actor / ruleset-re-enable work was DROPPED from this task and
  spun out (see Follow-ups). The app is NOT a bypass actor.
- `[bot]` suffix is GitHub-mandatory on app-generated actors.

## Proposal (delivered)

Created the **callabloom** GitHub App (kaukea-owned, App ID 4354752, signs `callabloom[bot]`;
Contents/Issues/PRs/Workflows = R/W; webhook off; installed on kaukea/orchids), stored its id +
private key as kaukea ORG secrets, and wired a per-hop app-token mint into the cloud path:
`actions/create-github-app-token@v3` behind the optional org secret (guarded by a job-level
`env` var, since `secrets` isn't available in step `if:`), routing `GH_TOKEN` + the git
push/commit identity through the minted token, with a
`${{ steps.app-token.outputs.token || github.token }}` fallback so nothing breaks before the
app/secrets exist. Applied to all four `cloud-path.yml` hops (plan/build/revise/close) and
`board-sync.yml`. Commit authorship resolves the bot user id at runtime →
`<id>+callabloom[bot]@users.noreply.github.com`.

Scope boundary: the app-creation web/admin steps were OPERATOR-authorized and driven live via
the ClaudeCodeBrowser MCP (registered at user scope). Consuming-repo rollout stays deferred.

## Testing

Agreed method (operator): live-fire — a cloud hop must act as `callabloom[bot]`.
RESULT — **PASS** (2026-07-21): `gh workflow run cloud-path.yml --ref f/app-identifying
-f hop=plan -f issue=23` → run 29825470361 completed/success; the newest gh#23 comment is by
`callabloom[bot]` (not `github-actions[bot]`), proving the token minted and the identity holds.
(The close-spine clauses in the original method were dropped with the spun-out ruleset work.)

## Result

Result: **done** · branch `f/app-identifying` @ HEAD 29c4c3e (🎉 anchor, `Base: 59abcc9`) ·
tested via live-fire workflow_dispatch on gh#23 → PASS (hop posted as `callabloom[bot]`) ·
callabloom app (App ID 4354752) created + installed on kaukea/orchids + org secrets set +
private key backed up in Bitwarden. Follow-ups spawned below.

## Changelog entry (staged — orchestrator places at ingest, Decision-034)

- 🪪 The cloud hops now speak as **`callabloom[bot]`** — a kaukea GitHub App (App ID 4354752)
  minted per hop from org secrets, replacing the anonymous `github-actions` actor; falls back to
  the built-in token when the secrets are absent (`cloud-path.yml` all hops + `board-sync.yml`).

## Readme delta (staged)

- No change (evidenced). README covers the cloud path only narratively (line 91, "the spine runs
  on issue comments") and documents no cloud-path setup, secrets, or actor identity; the callabloom
  app + org secrets are operational admin details README does not state, so nothing there goes stale.

## Architecture

- EDITED (trigger fired — auth substrate / how the hops connect to GitHub). `ARCHITECTURE.md`
  §The cloud path now records that the hops act on GitHub as `callabloom[bot]` (a kaukea GitHub
  App token minted per hop from org secrets, fallback the built-in token), distinct from
  `CLAUDE_CODE_OAUTH_TOKEN` (which auths the Claude CLI).

## Follow-ups (spun out — for the orchestrator to board)

- **branch-protection as code** — require operator approval to merge `main` (via code-owners),
  callabloom excepted; formalise the *existing* close rules, NOT a status-check/bypass contraption.
- **orchestrator-in-the-cloud + merge ordering ("Mr. Rabbit")** — deterministic merge order ==
  changelog order; a merge queue (or optimistic-retry) owns it; changelog/readme applied at the
  serialized merge against current main; the loop closes by calling the orchestrator. Minor-change
  close model: housekeeper prewrites; the serialized merge moves the notes onto the squash.
- **launcher subagent** — extract git-worktree creation + agent launching from the local
  orchestrator into its own subagent (owns the local-vs-remote seam; remote = no-op).
- **cloud agents express deltas** — issue-thread agents should post the change, not re-paste their
  prior message with a correction.
- **Routine (Anthropic cloud agent) NL-trigger** — a routine that dispatches the GH Actions
  workflow (research-preview; can't own identity — routines act as the user's account).
- **sidebar board hygiene** — the live-fire showed gh#23's `session-naming` blocker still open
  though session-naming is done; the fleet-sidebar sidecar needs its blocker cleared.
- **hard rule (relayed to orchestrator, operator directive)** — operator-expected actions must be
  bulleted at the END of an interaction, never buried mid-description of an agent's work.
