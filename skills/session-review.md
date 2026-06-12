# Skill: session-review ⭐ (the meta-loop)

**Trigger:** nightly. **Goal:** the system improves from its own failures while everyone sleeps. This is the skill that makes the OS self-evolving — if only one automation runs, it's this one.

1. Read since last run: `logs/sessions/`, `logs/gate-failures.md`, workflow run logs, the triage log.
2. For each failure or friction point, diagnose the cause — one of:
   - **missing context** → which brain page should have had it?
   - **stale context** → which page lied?
   - **missing/weak tool** → what capability was absent?
   - **weak skill** → which instruction was unclear or wrong?
   - **missing gate check** → what should the checklist have caught?
3. **Ship safe fixes autonomously** (per the self-modification boundary in `rules.md`): add/correct brain context, clarify skill instructions, add checks to `reviews/` checklists, fix broken links.
4. **Queue risky fixes** for human approval in `dream/CHANGELOG.md` under "Pending approval": anything loosening a permission, changing what gets sent externally, or retiring a workflow.
5. Log every change made (file, what, why) in `dream/CHANGELOG.md`. Unlogged self-modification is forbidden.
6. Also check: did every scheduled cron actually run? Dead automations get flagged in the morning brief — a self-evolving system whose evolution silently stopped is the worst failure mode because nobody notices.
