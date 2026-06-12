# logs/ — what the system learns from. Append-only.

If it isn't logged, the nightly session-review can't learn from it. This folder is the meta-loop's food.

- `gate-failures.md` — every quality-gate decision (pass AND fail), one line each
- `sessions/` — 5-line summary per agent session (see AGENTS.md end-of-session protocol)
- `triage-log.md` — what inbox-triage filed where
- `briefs/` — morning briefs
- `install-progress.md` — install state (created during day 0)
- workflow run logs — one line per run: date, workflow, outcome, gate result

Append-only. Never edit or delete log history — the system's memory of its own mistakes is its most valuable training data.
