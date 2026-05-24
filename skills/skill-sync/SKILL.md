---
name: skill-sync
description: "MUST be read before starting any task, plan, or coding work, and again when finishing, for skills with `share: github`. Sync at workflow start, at workflow end, and on any code update in between. Errors are ignored. This should trigger alongside workflow."
metadata:
  share: github
---

# Skill Sync

Skills are shared across projects and must stay consistent.

## Checklist

- [ ] `dotai sync` run at workflow start
- [ ] `dotai sync` run on any code update in between
- [ ] `dotai sync` run at workflow end

## When to sync

Synchronize the skills and agent instructions:

```bash
dotai sync
```

Run `dotai sync`:

- at workflow start
- at workflow end
- on any code update in between (commit, edit, refactor — any change to source)

Errors from `dotai sync` are ignored; the workflow proceeds regardless.
