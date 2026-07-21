- created: 2026-07-21
- created_by: fable-5
- created_during: f/app-identifying

## Blockers

- None.

## Questions

- To scope when picked up.

## Findings

- Observed in the cloud live-fires: issue-thread agents re-paste their prior
  message with a correction instead of posting what changed — noisy threads,
  buried deltas.

## Proposal

Cloud/issue-thread agents express the DELTA: post the change against their
prior comment, never a corrected re-paste of the whole message.

## Testing

To agree when ripened.
