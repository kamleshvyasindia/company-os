# Workflow: feedback-to-linear

- **Department:** product
- **DRI (named human):** [[people/ENGINEER]]
- **Status:** draft — installed YYYY-MM-DD

## Sensor
Daily 18:00 — new user-feedback messages in Slack since last run.

## Policy
- Classify each item: bug / feature request / confusion / praise.
- Bugs and confusions become **drafted** Linear issues (never auto-created — see gate).
- Duplicates: search Linear first; add a comment draft to the existing issue instead of a new one.
- Every draft links back to the source Slack conversation and the [[brain/customers/...]] page.

## Inputs
Slack user channels · Linear (read) · `brain/customers/`

## Tools
Slack (read), Linear (read; **create = ask-first** until 2 weeks of clean gate history, then canvas may be upgraded to draft-state creation).

## Output artifact
`departments/product/outputs/YYYY-MM-DD-feedback-triage.md` — classified list + drafted issues + duplicate notes.

## Quality gate
`reviews/data-checklist.md`: correct classification spot-check, no duplicate creation, repro steps present for bugs.

## Learning (write-back)
- Recurring themes (3+ mentions) → flagged in the triage file as roadmap signals
- Customer pages updated with what they reported

## Retire / revise when
Feedback volume justifies a dedicated support OS, or Linear workflow changes.
