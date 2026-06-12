# CRONS.md — the automation stack that makes this self-evolving

Six layers. **Start with the Minimal Five** (marked ✦) — a complete sense→learn→fix→report circuit. Add the rest when their absence hurts; the nightly session-review will tell you, because that's its job.

Scheduling: use your harness's native scheduler (Claude Code scheduled tasks, system cron, Codex automations). No scheduler? Run them as ritual prompts — morning: brief; evening: triage + review. The system works either way; automation just removes the human from the trigger.

## Layer 0 — Capture (sensors → inbox)

| Cron | Cadence | Reads → Writes |
| --- | --- | --- |
| ✦ meeting-capture | per meeting | recorder → `inbox/` (skill: `skills/meeting-capture.md`) |
| slack-sweep | daily | user/feedback channels → `inbox/` |
| metrics-pull | daily | analytics/payments → `logs/metrics/` |
| market-sweep | weekly | competitors/market → `inbox/` |

## Layer 1 — Triage (inbox → brain)

| Cron | Cadence | What |
| --- | --- | --- |
| ✦ inbox-triage | nightly | file captures into entity pages (skill: `skills/inbox-triage.md`) |
| entity-enrichment | nightly | new people/companies get filled in |

## Layer 2 — Brain hygiene

| Cron | Cadence | What |
| --- | --- | --- |
| dedup-sweep | weekly | merge duplicate entity pages |
| contradiction-check | nightly | flag brain pages that disagree |
| staleness-sweep | weekly | flag load-bearing pages untouched 6+ weeks |

## Layer 3 — Workflow operation

Each workflow's **sensor** is its own trigger (event or schedule), defined in its canvas. Built-in rule, not a cron: ✦ **every gate decision appends to `logs/gate-failures.md`** — the meta-loop's food.

## Layer 4 — The meta-loop (what makes it self-EVOLVING)

| Cron | Cadence | What |
| --- | --- | --- |
| ✦ **session-review** ⭐ | nightly | logs → diagnose failures → ship safe fixes, queue risky (skill: `skills/session-review.md`) |
| skill-improvement | weekly | usage transcripts → skill edits, keep what scores better |
| resolver-hygiene | weekly | DRY + MECE check across skills/tools |
| workflow-health | weekly | failure rate, gate-catch rate, staleness per workflow → revise/retire flags |
| integration-health | daily | ping every connector — expired auth producing garbage quietly is the #1 silent killer |

## Layer 5 — Reporting & regeneration

| Cron | Cadence | What |
| --- | --- | --- |
| ✦ morning-brief | daily | ran / caught / changed overnight / needs you / today (skill: `skills/morning-brief.md`) |
| weekly-scoreboard | weekly | scoreboard refresh + founder review packet (skill: `skills/weekly-scoreboard.md`) |
| playbook-regen | monthly | regenerate strategy briefs/playbooks from ALL accumulated data; regenerate disposable dashboards |
| maturity-audit | quarterly | score against the 5-stage ladder; re-forecast; re-ask the doctrine litmus question |

## Two rules that hold it together

1. **Write-permission boundary:** Layers 0–2 and 5 write freely (brain, logs, reports). Layer 4 may autonomously change skills/reviews/brain only in safe ways; anything loosening permissions or touching external sends goes to the approval queue in `CHANGELOG.md`. (Full boundary: `rules.md`.)
2. **Every cron logs its own run.** The session-review checks for dead crons — a self-evolving system whose evolution silently stopped is the failure nobody notices for a month.
