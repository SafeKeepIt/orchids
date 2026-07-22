# Sidebar polish: the second corrective round from the operator's live pass

- created: 2026-07-22
- created_by: Sebastien Lambla

## Blockers

- None hard. Independent of the [[sidebar-fixes]] close — that task gates on its
  own recorded result; this round collects everything the operator's live pass
  found beyond it.

## Questions

- Per-agent colors: match Claude Code's subagent palette (red/blue/green/
  yellow/purple/orange/pink/cyan) — confirm terminal rendering fidelity is
  acceptable in the sidebar's tmux pane before committing to exact hues.
  CANNOT be resolved by code reading — no rendering test harness exists in
  the sidebar tooling (`tools/sidebar.py`, `tools/sidebar_model.py` on
  `f/sidebar-fixes`) and 256-color vs truecolor tmux fidelity is a visual
  call. Recommendation: implement against the 8 named ANSI colors first
  (portable everywhere); operator eyeballs the live pane and calls out any
  hue that reads wrong once the sidebar-fixes build is mounted.
- ~~Bus singleton: design question?~~ RULED (operator, 2026-07-22,
  Decision-051): the bus sidecar is a singleton PER AGENT — exactly one
  each, duplicates/orphans are the defect, correctived in
  [[bus-singleton]]. This round renders exactly one bus row per live
  agent: top of the list, italic, greyed, 📬.
- Emoji set for the status vocabulary (operator invites proposals; current
  proposal in the item below).
- /orchard `add <path>`: what counts as "an orchids installation in
  progress" at a path. CANNOT be resolved by code reading — no `/orchard`
  command exists yet anywhere in the tree (checked `f/sidebar-fixes` and
  main; only the design sidecars [[orchard]]/[[orchard-launch]]/
  [[orchard-view]]/[[orchard-summary]] exist, no implementation file).
  Confirmed from `.ai.toml` (kauk-managed, present at repo root): its
  presence is the only unambiguous "installed" signal today — there is no
  existing notion of a "partial manifest laydown" state to detect against.
  Recommendation: `add <path>` reports "present" iff `<path>/.ai.toml`
  exists, "not an orchids install" otherwise; defer any partial/in-progress
  state to a later round once `orchard` itself ships and a real partial-
  install case is observed. Needs operator confirmation before `add` is
  built.

## Findings

- Operator live pass, 2026-07-22, on the sidebar-fixes branch build mounted in
  his window. Some of the duplicate bus rows observed were real duplicates:
  the orchestrator session that morning had spawned a second bus sidecar by
  mistake, so multiplicity was partly genuine process noise, not only a
  display defect.
- "app-identifying" as a permanent first row: that feature closed 2026-07-21 —
  the row is stale state (likely a leftover bus/state file); the fix should
  find and clear the source, not just hide the label.

## Proposal

The operator's itemized list, verbatim in substance:

1. **Drop the hourglass** ("sablier") task animation entirely — each time it
   disappears the task text shifts left and back. No spinner glyph; layout
   must never shift with state.
2. **Hide internal rows**: "app-identifying" (always first, internal, stale —
   see Findings) and the bare session-UUID row. Neither is operator-facing.
3. **Subagent aggregation**: only the first feature ever shows subagents —
   every agent's subagents must render under their own parent row.
4. **Per-agent color**, matching Claude Code's subagent color palette where
   the terminal allows (see Questions).
5. **Buses**: shown at the TOP, italic, greyed, with a message icon (📬
   proposed) — they are expected to always be there; exactly ONE row per
   live agent (the per-agent singleton, Decision-051), none for dead
   agents; duplicates never render.
6. **Auto-mount**: the orchestrator mounts the sidebar the moment it first
   launches work — no manual mount step.
7. **Commands**: `/orchard show|hide|add <path>`, where `add` detects whether
   an orchids installation is actually present/in progress at the path.
8. **Ellipsis before clipping**: truncated row text (e.g. "agent-closing
   Done, awaiting…") shows an ellipsis, never a hard cut.
9. **Status vocabulary**, exactly three live states plus one parked state:
   - **working** 🚧 — the agent has active subagents or is working itself;
   - **waiting** — an external component is taking time (threshold ~5s);
     proposed glyph ⏱️ (static, fixed-width — no animation per item 1);
   - **done** ✅;
   - **awaiting another agent** — distinct glyph in very light gray to read
     as "not started yet"; proposed 🪷 (a closed bloom, dim) or 💤.
10. **Project header rendering**: the project title centered over a
    background GRADIENT rendered with half-block cells (▀▄), in the
    traditional orchid colour (the classic orchid #DA70D6 family) — except
    PAUSED projects, which render a very light gray instead of the gradient.
    Technique (operator, 2026-07-22): a half VERTICAL cell whose foreground
    and background step darker/lighter along the gradient direction, text
    drawn on top; a reference implementation exists in the seb.house
    repository (believed near the tmux/vt tooling, e.g.
    `~/src/serialseb/seb.house/deb/pi/vt/`) — reuse its approach but NOT
    animated.
11. **Title derivation is inconsistent** (bug): observed "claude" as the
    main title followed by the project name, and elsewhere the repo followed
    by the project name and a subtitle — no discernible logic. Define ONE
    deterministic scheme and fix every announcing source. Proposal: main
    title = the feature/project human name, subtitle = current activity;
    the program name ("claude") NEVER appears; a session with no announced
    name yet shows the repo name dimmed until its announce lands.
    SCOPE LIMIT (operator, 2026-07-22): the title scheme applies ONLY to
    orchid-managed tabs/windows — the operator keeps separate personal tabs
    that this change must never touch.
    GRAMMAR (operator, 2026-07-22): deriving the human name from a task id
    is a GRAMMATICAL conversion, not a mechanical dash-to-space — the
    imperative-vs-declarative rule as ORIGINALLY specified in the naming
    contract ([[session-naming]], gh#34): ids carry the imperative/verbal
    form, displayed titles are DECLARATIVE noun phrases — e.g.
    `field-projecting` renders as "field projection" — wherever titles are
    displayed.

## Testing

Operator visual pass on the live sidebar (the method that produced this list),
plus unit coverage for the model changes: internal-row filtering, per-parent
subagent aggregation, bus collapsing, truncation with ellipsis, the
three-plus-one status vocabulary including the 5s waiting threshold, the
paused-project gray vs orchid-gradient header path, and the deterministic
title scheme (never the program name; dimmed repo name pre-announce).
