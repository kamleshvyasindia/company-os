# RESOLVER.md — skill index

The routing table. Before doing any recurring task, check here for an existing skill. Before adding a skill, check it doesn't overlap an existing one.

| Skill | Does | Cadence | Writes to |
| --- | --- | --- | --- |
| `meeting-capture.md` | sync transcript → inbox → meeting page (decisions, commitments) | per meeting | inbox/, brain/meetings/, brain/decisions/ |
| `inbox-triage.md` | files inbox items into brain entity pages | nightly | brain/* |
| `morning-brief.md` | yesterday's runs + failures + overnight changes + today's prep | daily | logs/briefs/ |
| `session-review.md` ⭐ | reads logs → diagnoses failures → ships safe fixes, queues risky | nightly | skills/, reviews/, brain/, dream/CHANGELOG.md |
| `weekly-scoreboard.md` | refreshes scoreboard + founder review packet | weekly | scoreboard.md |
| `skillify.md` | turns work just done into a new skill + runs this hygiene check | after notable work | skills/ |

## Hygiene: DRY + MECE

- **DRY:** one skill per job. If a new skill overlaps an existing one, merge them — one skill with parameters beats two cousins.
- **MECE:** the table above should cover the recurring work with no gaps and no overlaps. The `skillify` skill runs this check every time something is added.
- Skills improve from use: when a skill's output gets corrected, the correction belongs IN the skill file (the session-review does this nightly).

## The skillify ritual

Done something twice? Say "skillify it." The agent writes the skill file from the session transcript, adds the row here, and runs the DRY/MECE check. This ritual is doctrine mandate #6 — it's how the company's know-how leaves heads and enters the system.
