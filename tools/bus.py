#!/usr/bin/env python3
"""Repo-scoped agent message bus.

The envelope lives here and nowhere else. Agents never construct or parse a
message: the bus sidecar shells out to this script on both send and receive, so
the format cannot drift across prompts and cannot be got wrong by an agent
following prose.

Layout (uncommittable, git-common-dir, so every worktree of the repo shares it):

    <git-common-dir>/the-works/bus/<agent-id>/<datetime>.json

The set of folders IS the registry — an agent exists for messaging purposes iff
its folder does. Broadcast writes a copy into each. Messages are ephemeral and
deleted on consumption, so receiving is "take what is there", with no bookkeeping.

Usage:
  bus.py init <agent-id>                       create this agent's inbox
  bus.py teardown <agent-id>                   remove it (session end)
  bus.py list                                  registry: one agent id per line
  bus.py send --from A --to B --type t --body X [--visible]
                                               [--request-id R] [--in-reply-to R]
  bus.py broadcast --from A --type t --body X [--visible]
  bus.py receive <agent-id>                    drain: JSON array, oldest first
  bus.py root                                  print the bus root
"""
import argparse
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

TYPES = ("post", "broadcast", "request", "reply", "status")


def bus_root() -> Path:
    gcd = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return (Path(gcd).resolve() / "the-works" / "bus")


def inbox(agent_id: str) -> Path:
    if not agent_id or "/" in agent_id or agent_id.startswith("."):
        sys.exit(f"bus: invalid agent id {agent_id!r}")
    return bus_root() / agent_id


def stamp() -> str:
    # sortable and readable; ':' avoided so the name is portable
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S.%f")


def deliver(target: Path, envelope: dict) -> None:
    """Write atomically: a watcher must never observe a half-written message."""
    target.mkdir(parents=True, exist_ok=True)
    final = target / f"{stamp()}.json"
    tmp = target / f".{final.name}.partial"
    tmp.write_text(json.dumps(envelope, indent=2), encoding="utf-8")
    os.replace(tmp, final)          # atomic; fires the watcher's moved_to


def envelope_of(args, to: str) -> dict:
    return {
        "id": uuid.uuid4().hex[:12],
        "ts": datetime.now(timezone.utc).isoformat(),
        "from": args.sender,
        "to": to,
        "type": args.type,
        "visible": bool(getattr(args, "visible", False)),
        "request_id": getattr(args, "request_id", None),
        "in_reply_to": getattr(args, "in_reply_to", None),
        "body": args.body,
    }


def cmd_send(args) -> None:
    target = inbox(args.to)
    if not target.is_dir():
        sys.exit(f"bus: no such agent {args.to!r} (no inbox) — is it running?")
    deliver(target, envelope_of(args, args.to))


def cmd_broadcast(args) -> None:
    root = bus_root()
    if not root.is_dir():
        sys.exit("bus: no bus root — nothing to broadcast to")
    peers = [d for d in sorted(root.iterdir()) if d.is_dir() and d.name != args.sender]
    for peer in peers:
        deliver(peer, envelope_of(args, peer.name))
    print(f"broadcast to {len(peers)} agent(s)")


def cmd_receive(args) -> None:
    box = inbox(args.agent_id)
    out = []
    if box.is_dir():
        for f in sorted(box.glob("*.json")):        # lexical == chronological
            try:
                out.append(json.loads(f.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, OSError) as exc:
                out.append({"type": "malformed", "file": f.name, "error": str(exc)})
            f.unlink(missing_ok=True)               # ephemeral: consumed is gone
    print(json.dumps(out, indent=2))


def cmd_init(args) -> None:
    box = inbox(args.agent_id)
    box.mkdir(parents=True, exist_ok=True)
    print(box)


def cmd_teardown(args) -> None:
    box = inbox(args.agent_id)
    if box.is_dir():
        for f in box.iterdir():
            f.unlink(missing_ok=True)
        box.rmdir()
    print(f"removed {box}")


def cmd_list(args) -> None:
    root = bus_root()
    if root.is_dir():
        for d in sorted(root.iterdir()):
            if d.is_dir():
                print(d.name)


def main() -> None:
    p = argparse.ArgumentParser(description="repo-scoped agent message bus")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name, fn in (("init", cmd_init), ("teardown", cmd_teardown)):
        s = sub.add_parser(name)
        s.add_argument("agent_id")
        s.set_defaults(func=fn)

    s = sub.add_parser("receive")
    s.add_argument("agent_id")
    s.set_defaults(func=cmd_receive)

    sub.add_parser("list").set_defaults(func=cmd_list)
    sub.add_parser("root").set_defaults(func=lambda a: print(bus_root()))

    def msg_args(s):
        s.add_argument("--from", dest="sender", required=True)
        s.add_argument("--type", default="post", choices=TYPES)
        s.add_argument("--body", required=True)
        s.add_argument("--visible", action="store_true",
                       help="surface to the operator, not just the agent")
        return s

    s = msg_args(sub.add_parser("send"))
    s.add_argument("--to", required=True)
    s.add_argument("--request-id", dest="request_id")
    s.add_argument("--in-reply-to", dest="in_reply_to")
    s.set_defaults(func=cmd_send)

    s = msg_args(sub.add_parser("broadcast"))
    s.set_defaults(func=cmd_broadcast, to=None, request_id=None, in_reply_to=None)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
