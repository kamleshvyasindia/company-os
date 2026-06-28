# Tool Registry

What agents can call, at what tier. **Connector/MCP first, browser second, computer-use last.** Everything starts `read`; write access is earned per-workflow (granted in the workflow's canvas, never globally).

Tiers: `read` (look, never touch) → `draft` (create drafts/staging, never send) → `act` (perform scoped actions; canvas-granted only).

| Tool | Purpose | Access path | Tier | Status | Since |
| --- | --- | --- | --- | --- | --- |
| Slack | internal comms + user feedback (primary sensor) | connector/MCP | read | ☐ not connected | — |
| Meeting recorder | daily sync transcripts → inbox | export/API | read | ☐ not connected | — |
| Linear | engineering issues | connector/MCP | read | ☐ not connected | — |
| GitHub | code + this repo | git CLI | read | ☑ connected | 2026-06-28 |
| Gmail | external comms | connector | read | ☐ not connected | — |
| Analytics / payments | scoreboard data | connector/API | read | ☐ not connected | — |
| Notion | project management & client docs | browser/manual | read | ☐ not connected | — |
| WhatsApp | client & team messaging | browser/manual | read | ☐ not connected | — |

## Adding a tool

1. Add the row here (tier = `read`) with date.
2. Run a live read test; paste the test query + result summary below the table.
3. Only a workflow canvas may raise the tier, and only for its own runs.

## Live Read Tests

- **GitHub / Git CLI (2026-06-28)**:
  - *Query*: `git log -n 3`
  - *Result*: Successfully retrieved recent commits. Output includes:
    ```
    commit 4fe6f2c979d136e820a344019947a12dc65c3d42
    Author: Data Science with Harshit <datasciencewithharshit@gmail.com>
    Date:   Sun Jun 14 04:27:38 2026 +0530

        Add teammate onboarding: ONBOARD_FOR_AGENTS.md + scoped department AGENTS.md
    ```

## The first 10× tool

If you connect only one thing, connect **read access to your own data** (Slack + analytics). The unlock isn't automation — it's that everyone starts asking questions they never bothered to ask before.
