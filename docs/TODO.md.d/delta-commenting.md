- created: 2026-07-21
- created_by: fable-5
- created_during: f/app-identifying

## Blockers

- None.

## Questions

- Enforcement point, to settle when picked up: which charters/prompts carry the
  conversational rule — the cloud hop prompts foremost; do local agents' issue
  and PR comments follow the same contract?

## Findings

- Observed in the cloud live-fires: issue-thread agents re-paste their prior
  message with a correction instead of posting what changed — noisy threads,
  buried deltas.
- Operator scope (2026-07-21): interventions in conversational agentic issue and
  pull-request discussions must be more HUMAN-LIKE — never repeating the same
  content with corrections; continue the conversation, acknowledging and
  offering advice, so the issue is refined in place instead of specifications
  being republished.

## Proposal

Agent interventions in issue and pull-request discussions read like a human
participant continuing a conversation, not a bot republishing documents:

- acknowledge what the thread has established, then add what CHANGES — the
  delta, never a corrected re-paste of a prior message;
- offer advice and refinements as conversation, so the issue itself is refined
  through the thread instead of specifications being republished wholesale.

## Testing

To agree when bloomed.
