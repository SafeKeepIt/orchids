- created: 2026-07-17
- created_by: opus-4.8

## Blockers
- None known, but three capability questions below could each stop it dead (browser
  driving, Bitwarden unlock, email verification). Answer them before building.

## Questions
- **How does the agent drive the browser?** "Go to a site and create an account" needs a
  real browser: CAPTCHAs, JS forms, cookie walls. Playwright? An MCP browser tool?
  Or is the skill a *procedure the operator executes* with the agent generating and
  filing the secrets? The answer decides whether this is automation or a checklist.
- **How does Bitwarden get unlocked?** `bw` needs `BW_SESSION`. Where does the master
  password come from — operator prompt each run, or a keyring? A skill that stores
  secrets must not create a worse secret-handling problem than it solves.
- **Email verification loop.** Most signups send a confirmation link. The session has a
  Gmail connector (`mcp__claude_ai_Gmail__*`), which could read it for
  `monsterthatland@gmail.com` — but `seb@serialseb.com` is a different mailbox and may
  need another path. Does the skill wait for and click the link, or hand it back?
- **CAPTCHA / anti-bot.** Some sites will refuse automation outright. Is the skill
  allowed to stop and hand control to the operator, or is a site that CAPTCHAs simply
  out of scope? (Recommend: hand back — do not build evasion.)
- **Which emails are on the list**, and does the skill offer aliases (`+tag`,
  catch-all on serialseb.com) rather than only whole addresses?
- **Where does the DAG hang it?** Operator said "probably a web branch" — a `web` node
  in the role tree (Decision-003). Confirm: `web` as a new root, or under an existing
  node? Nothing in the current 26 skills is web-shaped, so this would be the first.

## Findings
- Operator's requirement, verbatim intent: ask **only** two things — the site, and which
  of their emails to use. Everything else (password generation, storage, OTP capture) is
  the skill's job. That "two inputs" constraint is the whole design goal; a skill that
  asks six questions has failed even if it works.
- Scope: generate a random password, create the account, capture any OTP/TOTP secret the
  site offers, and store password + OTP in Bitwarden.
- Bitwarden's CLI can generate the password (`bw generate`) and store a TOTP seed on an
  item, so the storage half is well-trodden. The signup half is where the risk is.
- **Secrets must never reach git.** Passwords and TOTP seeds are exactly the content
  `AGENTS.shared.md` bans from the tree. This skill's output belongs in Bitwarden and
  nowhere else — not in a sidecar, not in a log, not in a commit message. Relevant to
  `cross-repo-inbox`'s `refs/sensitive/<id>` work, but the simpler rule holds: the
  secret's home is the vault, so nothing needs to be written down at all.
- The corpus has no browser-driving skill today, so whatever answer question 1 gets is a
  new capability for the fleet, not a reuse.

## Proposal
A skill that, given a site and an email, runs: generate password → create account →
capture OTP if offered → store both in Bitwarden → report the item, never the secret.
Shape depends on the browser-driving answer; do not start until that is settled.

## Testing
End-to-end on a throwaway site the operator nominates: account exists, login works from
the Bitwarden entry, TOTP (if any) produces a code that authenticates. Assert the
password and seed appear nowhere outside the vault — grep the tree, the logs, and the
session transcript. Negative: a CAPTCHA site stops and hands back cleanly rather than
failing halfway with a half-created account and an unstored password.
