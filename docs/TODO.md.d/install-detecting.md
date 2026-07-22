# Install detecting: richer orchids-install state beyond .ai.toml presence

- created: 2026-07-22
- created_by: Sebastien Lambla
- created_during: sidebar-polish scope round

## Blockers

- The real kauk CLI shipping — today's stopgap has no install-state model to
  query; building richer detection against it would be throwaway.

## Questions

- (at pickup) what states the real kauk exposes: installed / partial laydown /
  in-progress / stale, and through what interface.

## Findings

- Ruled at the sidebar-polish scope round (operator, 2026-07-22): `.ai.toml`
  presence is the SUFFICIENT install signal for now; `/orchard add <path>`
  ships against it. This task exists because other repos will exist in the
  future and presence-only detection will eventually mislead (partial or
  in-progress installs read as absent or as fully installed).

## Proposal

When the real kauk lands, `/orchard add <path>` (and any other consumer of
"is this an orchids install?") distinguishes actual install states —
installed, partial, in-progress — via kauk's own state model instead of
`.ai.toml` presence alone.

## Testing

To agree at readiness, once the real kauk's state model is known.
