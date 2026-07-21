- created: 2026-07-21
- created_by: fable-5
- created_during: f/cloud-architect

## Blockers

- None.

## Questions

- To scope when picked up.

## Findings

- LOAD-BEARING (operator, 2026-07-21): the built-in Actions identity CANNOT be
  bypass-listed on a repo ruleset, so close-spine is DISABLED until a named
  kaukea GitHub App exists (operator name + orchid logo; [bot] suffix is
  GitHub-mandatory; minted per hop via actions/create-github-app-token, fallback
  github-actions). The app is simultaneously: the hops' visible identity, the
  PR-creation policy exemption, and the clean ruleset bypass actor.

## Proposal

Create the app, wire the per-hop token mint, put it on the bypass list, and
re-enable the close-spine ruleset.

## Testing

To agree when ripened — expected: a hop comments under the app identity and a
housekeeper merge passes close-spine while direct non-app pushes are rejected.
