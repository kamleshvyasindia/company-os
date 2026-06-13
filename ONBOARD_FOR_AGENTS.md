# ONBOARD_FOR_AGENTS.md — join an existing Company OS

You are onboarding a **new teammate** into a company OS that is already installed. Do **not** run `INSTALL_FOR_AGENTS.md` — that's day-0 founder setup and it would overwrite the company. This is the join path.

## What you need from the teammate (ask, one at a time)
1. Their name and role.
2. Which department they'll operate: `marketing` / `sales` / `support` / `product` / `ops`.
3. Which tools they personally need (the founder/admin confirms what they're allowed).

## Steps

1. **Confirm access.** You can read this repo. If you can't, stop — the founder must add this person as a collaborator on the private GitHub repo first (and grant them read access to the tools their role needs).
2. **Inherit the company.** Read `AGENTS.md`, `doctrine.md`, `rules.md`, and `brain/company.md`. The teammate now inherits the entire company context — they are not starting from zero, they are joining a brain that already knows the business.
3. **Read their lane.** Open `departments/<their-dept>/` and its `AGENTS.md`. These are the workflows they now own.
4. **Create their page.** Write `brain/people/<name>.md` (role, what they own as DRI, contact, working preferences). If it already exists, update it.
5. **Set their scope + tools.** Tell them which department OS they operate, which workflows are theirs, and connect **only** the tools their role needs (from `tools/registry.md`), read-only first. A marketing operator does not need Stripe; a CS operator does not need the ads account.
6. **Show the daily rhythm.** `git pull` (or let the agent do it) at the start → run their department's workflows → review outputs in the destination app (Slack drafts in Slack, etc.) → commit their outputs + session log back. Their agent handles the git plumbing; they talk to it in plain English.
7. **First task, together.** Run one of their department's existing workflows end-to-end with them watching — so they see a quality gate catch something and a real artifact get produced. That's the moment it clicks.

## Scope note — trust-by-default at small scale

Under ~10 people this is **one shared repo**. Everyone technically *can* see everything; each person operates their lane by convention (their department's `AGENTS.md`), not by hard walls. Do not build per-person permission infrastructure now — it's premature.

**The upgrade trigger:** when a teammate genuinely *shouldn't* see another department's data, OR a non-technical teammate can't comfortably use the git-repo flow and needs to just chat with the brain through a URL — that's when you stand up the hosted brain server (gbrain on Supabase) with real scoped access. Until one of those is true, the shared repo is the right answer.

## If the teammate is non-technical

Their only one-time technical steps are: install the coding agent (Codex or Claude Code) and authenticate it to GitHub once. After that, the **agent does all git operations** — clone, pull, commit, push — and they only ever talk to it in plain English. If even that is too much, it's the signal to move to the hosted brain server (a chat URL, no git at all).
