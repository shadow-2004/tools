#!/usr/bin/env python3
"""
tools :: monitor.py  (draft)

Snapshots the public timeline of a target X/Twitter handle on a schedule,
diffs each snapshot against the previous one, and appends every observed
change (NEW / DELETED / EDITED) to an append-only audit log.

The whole point: a post that gets deleted from the live timeline still
leaves a permanent trace in the audit log. Deletion != disappearance.
"""

import json
import hashlib
import datetime as dt
from pathlib import Path

TARGET = "soul_20004"          # https://x.com/soul_20004
AUDIT_LOG = Path("audit_log.jsonl")
STATE = Path(".state/last_snapshot.json")


def fetch_timeline(handle: str) -> list[dict]:
    """
    Return the current visible posts for `handle`.

    TODO: wire up a real source (official API bearer token, or a
    scraping backend). Returns a list of {id, text, created_at, media}.
    """
    raise NotImplementedError("plug in a data source before running")


def media_hash(media: list[str]) -> str:
    return hashlib.sha256("|".join(sorted(media)).encode()).hexdigest()[:16]


def load_previous() -> dict[str, dict]:
    if STATE.exists():
        return {p["id"]: p for p in json.loads(STATE.read_text())}
    return {}


def append_audit(event: str, post: dict) -> None:
    entry = {
        "observed_at": dt.datetime.utcnow().isoformat() + "Z",
        "event": event,                      # NEW | DELETED | EDITED
        "target": TARGET,
        "post_id": post["id"],
        "text": post.get("text"),
        "media": media_hash(post.get("media", [])),
    }
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def run_once() -> None:
    previous = load_previous()
    current = {p["id"]: p for p in fetch_timeline(TARGET)}

    for pid, post in current.items():
        if pid not in previous:
            append_audit("NEW", post)
        elif post.get("text") != previous[pid].get("text"):
            append_audit("EDITED", post)

    for pid, post in previous.items():
        if pid not in current:
            append_audit("DELETED", post)   # <-- the interesting one

    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(list(current.values()), ensure_ascii=False))


if __name__ == "__main__":
    run_once()
