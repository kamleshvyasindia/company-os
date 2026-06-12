# reviews/ — quality gates

One checklist per output type. Every workflow canvas names the checklist its output must pass **before a human sees it**. Every gate decision — pass or fail — is logged to `logs/gate-failures.md`.

Checklists grow from failures: when something bad slips through, the session-review adds a check here the same night. A checklist that hasn't grown in a month means either perfection or a dead gate — investigate.

Starter checklists: `writing-checklist.md` (content, posts, docs) · `comms-checklist.md` (anything sent to a human) · `data-checklist.md` (numbers, classifications, reports).
