# Digest identity: the telemetry routine publishes as callabloom

- created: 2026-07-22
- created_by: Sebastien Lambla

## Blockers

- None — the callabloom[bot] app identity exists and is live on the cloud path.

## Questions

- Route: (a) place the callabloom private key in the claude.ai cloud
  environment as a secret so the scheduled routine mints an installation
  token and publishes as callabloom[bot] — smallest change to what runs
  today; or (b) move the digest into a repo-scheduled GitHub Actions
  workflow that already holds callabloom credentials — but Claude in
  Actions bills via API key, unlike the claude.ai routine. Which?
- Destination: the digest currently lands as a PR only because the wiki
  push was refused (403). Keep PRs as the intended delivery, or pursue the
  wiki (which needs a non-app credential — see Findings), a committed
  file, or an issue?
- Where is the callabloom private key held today, and is the operator
  comfortable placing it in the claude.ai cloud environment (route a)?

## Findings

- The 2026-07-21 digest (PR #60, opened 2026-07-22T00:11:57Z) was
  published under the operator's own GitHub grant: PR author `serialseb`,
  commit 8fc7c2d author "Claude". The scheduled claude.ai routine pushes
  with the operator's credentials.
- The routine's wiki push returned 403 (permission denied); the PR was its
  fallback delivery.
- To verify during discovery: GitHub App installation tokens are believed
  not to work for wiki git operations (wikis sit outside the App
  permissions model), so switching identity to callabloom likely does NOT
  recover the wiki destination on its own — the wiki would need a machine
  credential of another kind.

## Proposal

The nightly telemetry digest publishes under the callabloom[bot] identity
instead of the operator's personal credentials — no digest artifact
(commit, branch, PR, comment) authored as the operator. The delivery
destination (PR vs wiki vs other) is settled by the Questions above and
becomes part of this task's scope.

## Testing

Observe the next scheduled digest run end-to-end: the digest branch,
commit, and PR are authored by callabloom[bot]; nothing in the run is
authored as the operator; delivery lands at the agreed destination.
