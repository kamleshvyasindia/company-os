# Company OS Seed

**A company operating system that installs itself.**

Clone this repo, point your coding agent at it (Claude Code, Codex — anything that reads files and follows instructions), and answer its questions. In about an hour you get: a Company Brain your agents can read and write, a tool registry, a skill registry, your first workflow loop with a quality gate, and the automations that make the whole thing improve while you sleep.

No knowledge-graph infrastructure. No database. No server. Markdown files in a git repo — readable by you, your cofounder, and every AI agent you'll ever use. When you outgrow this (and there are exact triggers for that below), you graduate to [gbrain](https://github.com/garrytan/gbrain). Until then, this is everything a small team needs.

Built for teams of 1–10. Works for non-technical founders: if you can answer questions in plain English, the agent does the rest.

## Quickstart

1. Clone this repo (or click "Use this template" on GitHub):
   ```
   git clone https://github.com/YOURNAME/company-os-seed my-company-os
   ```
2. Open it in Claude Code or Codex.
3. Paste this one line:
   ```
   Read INSTALL_FOR_AGENTS.md and follow it exactly.
   ```

The agent interviews you (one question at a time), seeds your Company Brain, connects your tools read-only, installs your first workflow with you, and sets up the daily rituals. You answer questions; it does the work.

## What's inside

```
company-os/
├── AGENTS.md               ← how agents operate here (the resolver — read first, every session)
├── CLAUDE.md               ← Claude Code compatibility shim
├── INSTALL_FOR_AGENTS.md   ← the day-0 install protocol
├── doctrine.md             ← 10 rules the FOUNDERS enforce (culture)
├── rules.md                ← what AGENTS may / must-ask / must-never do (permissions)
├── inbox/                  ← everything gets captured here first — append-only
├── brain/                  ← the Company Brain: one markdown page per customer, person, decision, meeting
├── departments/            ← each business function as a set of workflow loops (canvases)
├── tools/                  ← registry of what agents can call, with access tiers
├── skills/                 ← reusable know-how files + RESOLVER.md index
├── reviews/                ← quality-gate checklists
├── logs/                   ← gate failures, session summaries, workflow runs — what the system learns from
├── dream/                  ← the self-improvement layer: cron inventory + changelog of self-fixes
└── scoreboard.md           ← the numbers that keep this honest
```

## The idea in one paragraph

An AI-native company isn't a company that uses AI — it's a company that runs on an operating system of agents, context, and self-improving workflows, with humans owning judgment. Agents fail in most companies because the company is invisible to them. This repo makes your company *legible*: what you sell, who your customers are, what you decided and why, how work gets done, and what "good" looks like. Once that exists, every agent you point at it gets smarter — and the nightly review loop makes the system itself improve from its own failures.

## When you outgrow this → gbrain

This seed is deliberately minimal. Graduate to [gbrain](https://github.com/garrytan/gbrain) (Garry Tan's open-source brain — same markdown-first philosophy, plus hybrid retrieval, a self-wiring knowledge graph, and an automated dream cycle) when any of these fire:

1. **Retrieval misses** — "ask the repo" starts returning wrong/incomplete answers (typically a few hundred pages in).
2. **Entity questions** — "what's open across all customers?" — graph questions file-search can't answer.
3. **You want the dream cycle fully automated** instead of agent-run rituals.
4. **Headcount outgrows trust-by-default** and you need per-person scoped access.

Because this seed uses gbrain-compatible entity pages, migration is mechanical: `gbrain init` + import. Your markdown stays the system of record either way — that reversibility is the point.

## License

MIT. Fork it, run your company on it, make it better.
