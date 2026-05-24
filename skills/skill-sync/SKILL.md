---
name: skill-sync
description: "MUST be read before starting any task, plan, or coding work, and again when finishing, for skills with `share: github`. Pull before starting. If a shared skill was edited, collect it and push it when finishing. This should trigger alongside workflow."
metadata:
  share: github
---

# Skill Sync

Skills are shared across projects and must stay consistent.

## Checklist

- [ ] `dotai sync` run at workflow start (pull latest before editing anything)
- [ ] `dotai sync` run at workflow end (push edits before the squash lands)

## When starting and completing work

Synchronize the skills and agent instructions:

```bash
dotai sync
```
