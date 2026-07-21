#!/usr/bin/env python3
"""tmux navigation resolver for the fleet sidebar.

Resolves a tmux WINDOW by its `#{window_name}` and switches the operator's
client to it (session + window). Window name is the reliable handle —
pane titles get clobbered by a status-glyph setter (observed live:
`⠐ orchids ▸ fleet sidebar`), so matching is done on window name, not
pane title. Mirrors the resolve-by-title approach used by
tools/architect-teardown.sh, but runs on the AMBIENT tmux socket (the
sidebar lives inside the same tmux server it navigates), so plain
`tmux` is used rather than a `-S <socket>` target.

Window-name handles:
  - feature row -> "arch:<feature_id>"
  - repo row    -> "orch:<repo_name>"

STDLIB ONLY.
"""
from __future__ import annotations

import subprocess
import sys

LIST_WINDOWS_FORMAT = "#{session_name}\t#{window_id}\t#{window_name}"
LIST_PANES_FORMAT = "#{pane_id} #{pane_title}"


def _tmux(*args: str) -> str | None:
    """Run a tmux command, returning stripped stdout or None on any failure."""
    try:
        result = subprocess.run(
            ["tmux", *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _list_windows() -> list[tuple[str, str, str]]:
    """Return (session_name, window_id, window_name) for every window."""
    out = _tmux("list-windows", "-a", "-F", LIST_WINDOWS_FORMAT)
    if not out:
        return []
    windows = []
    for line in out.splitlines():
        # window names contain no tabs, so a plain split is exact.
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        session_name, window_id, window_name = parts
        windows.append((session_name, window_id, window_name))
    return windows


def resolve_window(name: str) -> tuple[str, str] | None:
    """Return (session_name, window_id) for the first exact window_name match."""
    for session_name, window_id, window_name in _list_windows():
        if window_name == name:
            return (session_name, window_id)
    return None


def resolve_pane(title: str) -> str | None:
    """Return the tmux pane id whose #{pane_title} equals `title`, or None.

    Kept for convenience/back-compat; NOT used by navigate() — pane titles
    are unreliable (clobbered by a status-glyph setter), so navigation
    matches on window name via resolve_window() instead.
    """
    out = _tmux("list-panes", "-a", "-F", LIST_PANES_FORMAT)
    if not out:
        return None
    for line in out.splitlines():
        pane_id, _, pane_title = line.partition(" ")
        if pane_title == title:
            return pane_id
    return None


def navigate(kind: str, key: str) -> bool:
    """Switch the tmux client to the window matching `kind`/`key`.

    kind is "repo" or "feature". Builds the window name ("orch:<key>" for
    repo, "arch:<key>" for feature), resolves it via resolve_window(), and
    if found switches the client to its session then selects the window
    (selecting the window focuses its active pane, which is sufficient).
    Returns True on success, False if no matching window was found (never
    raises, so a stale sidebar row can be ignored by the caller).
    """
    if kind == "repo":
        name = f"orch:{key}"
    elif kind == "feature":
        name = f"arch:{key}"
    else:
        return False

    match = resolve_window(name)
    if match is None:
        return False
    session_name, window_id = match

    if _tmux("switch-client", "-t", session_name) is None:
        return False
    if _tmux("select-window", "-t", window_id) is None:
        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: sidebar_nav.py <kind> <key>", file=sys.stderr)
        sys.exit(1)
    ok = navigate(sys.argv[1], sys.argv[2])
    print(ok)
    sys.exit(0 if ok else 1)
