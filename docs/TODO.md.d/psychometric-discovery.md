- created: 2026-07-20
- created_by: Sebastien Lambla

## Blockers

- None; builds on the scope round the handover contract defines ([[handover-contract]],
  Decision-025).

## Questions

- Which measurement techniques transfer: adaptive questioning (next question = the one
  that most reduces uncertainty about the intended feature, CAT-style), multi-item
  triangulation (several small probes instead of one broad "what do you want"),
  consistency checks across answers (flag contradictions as a reliability signal),
  forced-choice items to separate near-alternatives?
- What is the convergence criterion — when is the WHAT "measured" well enough to pass
  the WHAT-bar and stop asking?
- What triggers the instrument: operator says "fuzzy", or the orchestrator detects it
  (vague nouns, no testable outcome, conflicting constraints)?
- Where does it live: orchestrator definition, a dedicated skill the scope round loads,
  or prompts inside the readiness pipeline?

## Findings

- Operator suggestion (2026-07-20): apply psychometric test measurement logic to feature
  discovery when a feature seems fuzzy or not well defined. Context: the scope round
  (Decision-025) is where the WHAT gets defined; for fuzzy features a structured
  instrument beats free-form questioning — the same problem psychometrics solves for
  latent constructs (the intended feature is the latent variable; scope questions are
  the items).

## Proposal

- (to be shaped once the Questions are answered; expected: a fuzzy-feature question
  protocol the orchestrator runs inside the Decision-025 scope round)

## Testing

To agree at readiness: take one genuinely fuzzy feature through the instrument; the
resulting WHAT passes the bar and the build raises no scope question mid-flight.
