# rules.md — agent permissions

Company-wide defaults. Individual workflow canvases may grant additional, narrower permissions — never broader ones. Agents: you may not modify this file; propose changes to a founder.

## Never, under any circumstances (no exceptions, no asking)

- Send money, change billing, or touch payment systems.
- Delete or rewrite history in `inbox/`, `logs/`, or `brain/decisions/`.
- Modify `rules.md` or `doctrine.md`.
- Represent yourself as a human to a customer.

## Ask a named human first (default for anything irreversible or outward-facing)

- Send any external message: email, Slack DM to a user, social post, comment.
- Post or publish anything publicly.
- Create/close/modify issues in Linear or PRs in GitHub (unless a workflow canvas explicitly grants it).
- Modify any source-of-truth data in a connected tool.
- Contact anyone not already in `brain/people/` or `brain/customers/`.

## Allowed without asking (the default workspace)

- Read anything in connected tools at the tier set in `tools/registry.md`.
- Draft, summarize, research, classify, outline, organize.
- Create and update brain pages (cite your sources in the page).
- Append to `inbox/` and `logs/`.
- Run and improve skills; propose new ones via the skillify ritual.
- Build/modify disposable scripts and dashboards in department folders.

## Risk tiers (apply to every output)

| Tier | Examples | Handling |
| --- | --- | --- |
| 🟢 Green | summaries, internal drafts, research, brain updates | proceed; standard gate |
| 🟡 Yellow | customer-facing drafts, specs, data pulls for decisions | gate + human review in destination app |
| 🔴 Red | external sends, source-of-truth changes, money, legal | named human verifies; agent never acts alone |

## The self-modification boundary (for the nightly session-review)

The system may autonomously change **itself** only in safe ways: add context to brain pages, fix broken links/citations, clarify skill instructions, add checks to review checklists. Anything that loosens a permission, touches `rules.md`/`doctrine.md`, or changes what gets sent externally goes to the human approval queue in `dream/CHANGELOG.md`.
