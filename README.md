# tools

> OSINT toolkit — **draft / idea stage**

## Idea: `@soul_20004` leak monitor

**Target:** https://x.com/soul_20004

**Observation:** this account periodically posts *leaks* and then
**deletes** them within a short window. By the time anyone reacts, the
original post is already gone from the live timeline.

**Goal:** a watcher that snapshots the account timeline on a schedule,
diffs each snapshot against the previous one, and writes every
`NEW` / `DELETED` / `EDITED` post into an **append-only audit log** — so a
deleted post can never truly disappear.

### Why an audit log?

Because deletion only hides the post from the *live* timeline. A proper
audit log keeps the full record: timestamp, post id, text, media hash, and
the exact moment it was removed.

```
timeline  --snapshot-->  diff vs previous  -->  audit_log.jsonl (append-only)
```

### Planned components

| file            | purpose                                        |
|-----------------|------------------------------------------------|
| `monitor.py`    | poll the timeline, snapshot + diff             |
| `audit_log.jsonl` | append-only log of every observed change     |
| `notify.py`     | push an alert the moment a post is deleted     |

---

**Account to watch:** https://x.com/soul_20004
