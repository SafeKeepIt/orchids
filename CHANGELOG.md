# Changelog

## Work in progress

_base: `f65ad36`_

### ✨ New features

- 📋 Registry file set: README (the why/what) + ARCHITECTURE (the how) front
  door, the "install kauk/orchids" bootstrap contract
  (`Agent-installation.md`), and `docs/decisions.md` seeded with the
  history-rewrite charter.

### 🐛 Bug fixes

---

#### 📋 `f/registry-file-set` → `archive/registry-file-set`

Gives orchids its own registry file set: `README.md` sells the operating
model (agents, skills, rules as one versioned package), `ARCHITECTURE.md`
holds the mechanics, and `docs/decisions.md` opens with Decision-001 —
history migration is an orchestrator charter, gated by the project
`AGENTS.md` `repository:` field. The bootstrap contract becomes
"install kauk/orchids": `install.txt` renamed to `Agent-installation.md`,
with `index.html` (still served until the operator deletes the owin.org
remnants) regenerated to match. Close note: the branch was rebuilt at close
to repair a fabricated `Base:` SHA in its anchor commit; all work commits
and dates carried over verbatim.

_See `docs/TODO.md.d/registry-file-set.md` (findings & rulings) and
Decision-001 in `docs/decisions.md`._
