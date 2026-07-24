- created: 2026-07-24
- created_by: Sebastien Lambla
- completed: 2026-07-24
- completed_during: orchestrator

## Blockers

None — evidence is all in git history, archived branches, telemetry notes, and ingested
workstream logs.

## Questions

- ~~Verdict pending from the investigation (launched 2026-07-24, background): was the
  authoring agent's sidecar read directly or received as subagent summaries?~~
  Resolved same night: neither — no sidecar-driven authoring pass ever happened (see
  Findings).

## Findings

- The divergence being investigated: the bloomer's charter (Decision-027, promoted from
  the psychometric-discovery task) specifies a measurement instrument — adaptive
  questioning, consistency checks, a statistical convergence criterion, auto-kick. The
  built agent is a sidecar-fleshing clerk whose effective convergence criterion is
  "sections present", with triggers that depend on the orchestrator noticing a change
  signal.
- Operator hypothesis (stated 2026-07-24, ~90% prior, to be tested not assumed): the
  authoring architect never read its sidecar directly — instructions arrived as
  subagent summaries and attenuated. If confirmed, this is a live instance of the
  injection-integrity defect class ([[injection-integrity]], gh#28: instructions must
  arrive intact, not summarised).

- VERDICT (investigation completed 2026-07-24, 92% confidence): the summarization
  hypothesis is REFUTED for this artefact — no architect and no sidecar-driven build
  ever authored the charter-relevant shape. Timeline: the clerk was born 2026-07-01 in
  the TitanShield repo (commit 214ee7e), nineteen days BEFORE Decision-027 existed,
  and faithfully implements the charter it had then (TitanShield Decision-088,
  operator-ruled prep-only cut, six minutes after the build). Decision-027's encoding
  commit (205f50d, 2026-07-20) updated decisions.md, the sidecar, architect.md and
  orchestrator.md — everything EXCEPT the agent definition it chartered. Both
  subsequent renames (6ab9e38 groomer→ripener, 8444a85 ripener→bloomer) were
  word-swaps that grafted Decision-027 citations onto the unrebuilt clerk body. A blob
  census across all refs found exactly six variants, all accounted for — no lost
  psychometric build exists.
- Root defect class (routed to [[injection-integrity]]): PUSH/PULL CHANNEL MISMATCH —
  charters live in pull channels (decisions.md, sidecars) while agent behaviour rides
  the push channel (the agent definition), and nothing lints a charter against the
  artefact it governs. Corollary findings: "cites the ruling" is not "implements the
  ruling" (renames are a charter-drift vector); and the orchestrator — the role that
  executed every one of these commits — is forbidden from opening sidecars in steady
  state, a structural blind spot for exactly this gap.
- The summarization defect class itself remains real elsewhere (documented 2026-07-19:
  an architect treated a subagent's summary of a protocol document as sufficient) —
  it just did not produce this artefact.

## Proposal

Forensic reconstruction of how the bloomer got its shape: full git timeline of the
agent definition (including its pre-rename history), the charter and sidecar content as
they stood at each authoring commit, the architect definition's read-vs-summarize
protocol at the time, telemetry notes and surviving workstream logs from the authoring
feature. Deliverable: a timeline, an instructions-vs-built comparison, a verdict on the
summarization hypothesis with confidence and ranked alternatives, and implications
routed to [[injection-integrity]]. Read-only; findings land here, remediation is
scoped as follow-up tasks (likely: the bloomer rebuild chartered in the 2026-07-24
blueprint, plus injection-integrity hardening).

## Testing

Investigation task — the gate is evidential: every timeline claim carries a commit SHA
or file reference; the verdict states its confidence and what evidence would overturn
it.
