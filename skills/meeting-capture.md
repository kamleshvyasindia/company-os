# Skill: meeting-capture

**Trigger:** a meeting transcript exists (daily sync, user call). **Goal:** nothing said in a meeting is lost to the OS.

1. Save the raw transcript to `inbox/YYYY-MM-DD-<meeting>-transcript.md` (append-only).
2. Create `brain/meetings/YYYY-MM-DD-<meeting>.md` from the template: attendees (linked), decisions, commitments (who/what/when), open questions.
3. Every load-bearing decision ALSO gets its own page in `brain/decisions/` (template), linked from the meeting page.
4. Commitments involving a customer → update that `brain/customers/` page.
5. Reply with: decisions count, commitments count, anything ambiguous that needs a human's confirmation.

**Gate:** never paraphrase a decision into something stronger than what was said. Ambiguity gets flagged, not resolved silently.
