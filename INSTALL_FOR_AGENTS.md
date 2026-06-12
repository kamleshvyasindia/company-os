# INSTALL_FOR_AGENTS.md — Day-0 Protocol

You are an AI agent installing this Company OS for a founder. Follow the phases in order. Total time: ~60–90 minutes of the founder's attention.

## Rules for you, the installing agent

- **One question at a time.** Never present a wall of questions.
- **Plain language.** The founder may be non-technical. No jargon without a one-line explanation.
- **Never invent facts.** Everything you write into the brain comes from the founder's answers or connected tools. Unknowns get written as `GAP:` lines in the relevant page — gaps are valuable.
- **Confirm before writing.** After each phase, show a short summary of what you're about to write and get a yes.
- **If interrupted,** note progress in `logs/install-progress.md` and resume from there next session.

---

## Phase 0 — Preflight (2 min)

1. Confirm you can read and write files in this repo.
2. Read `AGENTS.md`, `rules.md`, and `doctrine.md` so you operate correctly from minute one.
3. Tell the founder: *"I'm going to interview you, set up your company's brain, connect your tools read-only, and install your first workflow. You answer questions; I do the work. Ready?"*

## Phase 1 — The interview (~15 min, one question at a time)

Ask, in order. Listen for entities (people, customers, tools) — you'll create pages for them in Phase 2.

1. What does the company sell, and to whom? (one paragraph)
2. Who is on the team? Name + role + what they own. (these become `brain/people/` pages and DRI candidates)
3. Who are your most important users/customers right now? Name 3–7. (→ `brain/customers/` pages)
4. Where does work happen? Which of these do you use: Slack, email, Linear/Jira, GitHub, Notion, WhatsApp, meeting recorder, analytics? Anything else?
5. What gets decided in your daily/weekly sync, and is it recorded? (if not recorded → flag: doctrine mandate #1)
6. What are the 3–5 tasks you or the team repeat every single week?
7. Which of those is the most painful or most often dropped?
8. What is the company's #1 focus for the next 90 days? (growth/marketing? product? revenue?) — this picks the first department.
9. What must an agent NEVER do without asking you? (seeds `rules.md` customization)
10. What numbers do you check to know the business is okay? (seeds `scoreboard.md`)
11. Anything an agent should know that isn't written anywhere? (tribal knowledge → brain)

## Phase 2 — Seed the brain (~10 min)

From the interview, write:

- `brain/company.md` — replace every `[PLACEHOLDER]`. Include explicit `GAP:` lines for what's unknown.
- `brain/offers.md` — what's sold, pricing, current state.
- `brain/people/<name>.md` — one page per team member (use `_template.md`).
- `brain/customers/<name>.md` — one page per named customer/user (use `_template.md`).
- `brain/decisions/` — any standing decisions mentioned in the interview, one page each.

Show the founder `company.md` and ask: "What's wrong or missing?" Fix it. This correction step matters more than the draft.

## Phase 3 — Connect tools, read-only first (~15 min)

For each tool from Q4, in this priority order: **connector/MCP first, browser second, computer-use last.**

1. Wire the connection (walk the founder through any auth screens).
2. **Test with a read query** ("show me the 5 most recent Slack messages in #general") and show the founder the result.
3. Record a row in `tools/registry.md`: tool, access path, tier = `read`, status, date.
4. Do NOT enable write/send for anything yet. Write access is granted per-workflow in Phase 4, per `rules.md`.

Typical small-team stack and what each is for:
- **Slack** — internal comms + user feedback conversations (sensor goldmine)
- **Meeting recorder** — the daily sync transcript → `inbox/` (mandate #1)
- **Linear** — engineering issues (product loop sensor)
- **GitHub** — code + this very repo
- **Gmail** — external comms
- **Analytics/payments** — the scoreboard's data source

If the team uses WhatsApp for anything that matters: recommend moving those threads to Slack — WhatsApp is invisible to the OS.

## Phase 4 — Install the first workflow (~20 min)

1. Take the answer to Q7/Q8 and propose ONE workflow to install first. Default suggestions by focus:
   - **Marketing focus:** `user-signal-to-content` — mine Slack user conversations weekly for pains/wins → content ideas + draft posts, gated by the writing checklist. (see the worked example in `departments/marketing/`)
   - **Product focus:** `feedback-to-linear` — classify user feedback from Slack → drafted Linear issues with links back to the source conversation.
   - **Revenue focus:** `follow-up-discipline` — unanswered external threads surfaced daily with drafted replies.
2. Copy `departments/_canvas-template.md` into the right department folder and fill it **with the founder**: sensor, policy, tools, gate, learning, DRI, retirement condition.
3. Create/adapt the matching checklist in `reviews/`.
4. **Dry-run it once now**, end to end, with the founder watching. Log the run to `logs/`. Fix what's clumsy.

## Phase 5 — Schedule the minimal automation set (~10 min)

Install these five rituals (full inventory: `dream/CRONS.md`). Use the harness's native scheduler if available (Claude Code scheduled tasks / cron / Codex automations); otherwise set them up as **daily ritual prompts** the founder pastes each morning — the system works either way, automation just removes the human from the trigger.

1. **meeting-capture** — every sync transcript lands in `inbox/` (skill: `skills/meeting-capture.md`)
2. **inbox-triage** — nightly: file inbox items into brain pages (skill: `skills/inbox-triage.md`)
3. **gate-failure logging** — built into every workflow run (verify it wrote to `logs/` during the Phase 4 dry-run)
4. **session-review** — nightly: read logs → diagnose failures → ship safe fixes, queue risky ones (skill: `skills/session-review.md`) ⭐ *this is what makes the OS self-improving*
5. **morning-brief** — daily: yesterday's runs + failures + overnight changes + today's prep (skill: `skills/morning-brief.md`)

## Phase 6 — Verify and hand off (~5 min)

Run these checks and show the founder the results:

- [ ] `brain/company.md` has no `[PLACEHOLDER]` left (GAP: lines are fine)
- [ ] Every team member and named customer has a brain page
- [ ] Every connected tool has a registry row and passed a live read test
- [ ] One workflow canvas is filled, dry-run, and logged
- [ ] The five rituals are scheduled (or the founder has the daily prompt saved)
- [ ] `scoreboard.md` has its baseline numbers
- [ ] The founders have read and signed `doctrine.md`

Then print a handoff summary: what was installed, the one workflow now live, the five rituals, and the suggested next workflow to install in week 2. Append the summary to `logs/install-progress.md`.

Welcome to the operating system. From here, every session follows `AGENTS.md`.
