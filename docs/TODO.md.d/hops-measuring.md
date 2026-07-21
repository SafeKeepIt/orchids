- created: 2026-07-21
- created_by: fable-5
- created_during: f/cloud-architect

## Blockers

- None.

## Questions

- To scope when picked up.

## Findings

- Hops run ~17-25 min with no wall-time record; dispatches lack resolved-id and
  branch hints, forcing each hop to re-derive them.

## Proposal

Measure hop wall-time (telemetry note or issue comment) and pass resolved
id/branch into dispatch inputs.

## Testing

To agree when ripened.
