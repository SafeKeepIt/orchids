- created: 2026-07-21
- created_by: fable-5
- created_during: f/cloud-architect

## Blockers

- None.

## Questions

- To scope when picked up.

## Findings

- Live-fire: gh-ingest created a stub for an issue that duplicated an existing
  board task (gh#23 / fleet-sidebar). Dedup at ingest per Decision-029: older
  task is the home; badge binds; stub never born.

## Proposal

board_gh pull recognises an issue matching an existing task and binds instead of
stubbing.

## Testing

To agree when ripened.
