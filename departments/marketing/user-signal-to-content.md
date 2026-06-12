# Workflow: user-signal-to-content (worked example)

- **Department:** marketing
- **DRI (named human):** [[people/FOUNDER]]
- **Status:** draft — installed YYYY-MM-DD

> The default first loop for a marketing-focused product team: your users are already telling you what to write. This loop mines real user conversations for pains, wins, and exact phrases, and turns them into content drafts — grounded in evidence, gated before any human time is spent.

## Sensor
Every Friday 09:00 — and ad-hoc when the founder runs it.

## Policy
- Only mine channels users actually talk in (e.g. `#feedback`, shared user channels). Internal banter is out of scope.
- Quote users verbatim where possible; **anonymize by default** — no names/companies in content without explicit permission.
- Ideas must trace to ≥1 real conversation (linked). No invented pains.
- Tone and banned words: per `brain/offers.md` positioning notes.

## Inputs
- Slack: user-facing channels (last 7 days)
- `brain/customers/` pages (context on who said it)
- `brain/offers.md` (positioning)
- previous runs in `outputs/` (don't repeat ideas)

## Tools
Slack (read), brain (read/write). No external posting — drafts only.

## Output artifact
`departments/marketing/outputs/YYYY-MM-DD-content-batch.md`:
1. Signal digest — pains/wins this week, each linked to its source conversation
2. 3–5 content ideas ranked by signal strength × fit
3. 1–2 full drafts (post/thread/email) for the top ideas

## Quality gate
`reviews/writing-checklist.md` — plus: every claim traces to a linked source; anonymization verified. Gate decisions → `logs/gate-failures.md`.

## May do without asking / must ask first
- May: read channels, draft, update customer pages with new signal.
- Must ask: anything that posts/sends; quoting a user identifiably.

## Learning (write-back)
- New pains/quotes → the relevant `brain/customers/` page
- Published-content performance (when known) → appended to the batch file — next runs rank ideas using it

## Retire / revise when
Users stop talking where we listen, or 3 consecutive batches produce nothing the founder publishes.
