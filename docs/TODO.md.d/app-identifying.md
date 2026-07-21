- created: 2026-07-21
- created_by: fable-5
- created_during: f/cloud-architect

## Blockers

- None.

## Questions

- ~~App name?~~ RULED (operator, 2026-07-21): **Kaukai** — comments sign as
  `kaukai[bot]`; orchid logo; kaukea-owned. (Supersedes the earlier
  operator's-name lean; GitHub app names must be globally unique and may not
  equal an existing user/org login.)
- ~~Where do the mint credentials live?~~ RULED (operator, 2026-07-21):
  ORG-level secrets on kaukea (app id + private key) — consuming repos inherit
  them when the deferred rollout lands; one mint point.

## Findings

- LOAD-BEARING (operator, 2026-07-21): the built-in Actions identity CANNOT be
  bypass-listed on a repo ruleset, so close-spine is DISABLED until a named
  kaukea GitHub App exists (minted per hop via actions/create-github-app-token,
  fallback github-actions). The app is simultaneously: the hops' visible
  identity, the PR-creation policy exemption, and the clean ruleset bypass
  actor.
- `[bot]` suffix is GitHub-mandatory on app-generated actors.

## Proposal

Create the **Kaukai** GitHub App (kaukea-owned, orchid logo, signs as
`kaukai[bot]`), wire the per-hop token mint into the cloud-path hops
(actions/create-github-app-token behind an optional secret, fallback
github-actions), put the app on the close-spine bypass list, and re-enable the
close-spine ruleset (id 19333120).

Scope boundary: the GitHub web/admin steps — app creation, logo upload,
install on kaukea/orchids, org-level secrets, bypass-list edit, ruleset
re-enable — are OPERATOR-executed account/admin operations; the architect
delivers them as ONE complete ordered sequence (with failure modes inline) and
owns the workflow wiring. Consuming-repo rollout stays deferred
(cloud-architect deferral).

## Testing

Agreed (operator, 2026-07-21): live-fire — the fleet-sidebar run (gh#23,
unblocked by session-naming) rides the cloud path under the new identity.
Pass = hops comment as `kaukai[bot]` · a housekeeper merge passes the
re-enabled close-spine · a direct non-app push is rejected.
