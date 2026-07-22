# Operator interacting: questions, gates and summaries as one typed exchange

- created: 2026-07-22
- created_by: Sebastien Lambla

## Blockers

- Sequencing only: builds on the question ask-path landing in
  [[sidebar-polish]] item 12 (the bus-message question with numbered
  options is the first kind of this envelope).

## Questions

- Envelope kinds and their sidebar markers: question (❓, numbered options),
  gate request (plan → MAKE IT SO, done → THAT IS ALL — which glyph?),
  summary/presentation (which glyph?). Others (progress reports, blockers)?
- ~~Rendering surface?~~ RULED direction (operator, 2026-07-22, "let's try
  it and see if it works"): the broker is a SCRIPT, not an agent — a
  question message on the bus triggers a token-free tool drawing a native
  tmux popup (numbered options) over the operator's CURRENT window; the
  keypress returns over the bus to the asker. Subagents have no harness-UI
  surface, so an agent broker would render via tmux anyway while paying
  tokens for zero judgment. First live trial ships with [[sidebar-polish]]
  item 12; this task generalises the envelope to gates and summaries once
  the trial holds.
- Fallback when tmux is absent, and whether gate requests ever render only
  in the agent's pane.
- Does the operator's ANSWER travel back over the bus too (operator types in
  the orchestrator pane, relay carries it operator-origin per Decision-047),
  making the whole exchange symmetric?
- Enforcement: same pattern as the question tools — presentation habits
  stripped from agent defs and replaced by the typed send?

## Findings

- Operator direction (2026-07-22): the enforced question path generalises —
  "this could unify the MAKE IT SO for example, that each agent decides to
  ask differently, or the multiple choice questions, or for that matter
  summaries." One protocol, uniform display, no per-agent invention.
- The operator-origin relay (Decision-047/049) already carries gate words
  upstream; this task gives the downstream half the same typed shape.

## Proposal

One typed operator-interaction envelope on the bus: kind (question | gate |
summary), payload, numbered options where applicable. Agents SEND the
envelope instead of inventing presentation; the orchestrator renders all
kinds uniformly in the operator's pane; the sidebar marks the waiting kind
with its glyph. Gate SEMANTICS are untouched — MAKE IT SO and THAT IS ALL
remain the operator's words, exactly as ruled; only their request and
display unify.

## Testing

To agree at readiness: one live feature driven end-to-end through the
envelope — a discovery question, a plan gate request, and the done summary
all arriving uniformly in the orchestrator pane with correct sidebar
markers, and the operator's answers/gate words flowing back unchanged.
