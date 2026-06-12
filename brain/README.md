# brain/ — the Company Brain

The business, written down so agents (and new humans) can operate from it. Markdown in git is the **system of record** — any index or retrieval layer built on top is disposable.

## The entity-page pattern

**One page per entity.** One file per customer, per person, per decision, per meeting — never monolithic lists. Link entities with `[[wikilinks]]`: `[[customers/acme]]`, `[[people/priya]]`, `[[decisions/2026-06-10-pricing]]`.

Why: pages-per-entity is what makes the brain *queryable* ("what's open with Acme?" reads one page, not a 2,000-line file), keeps git diffs meaningful, and is exactly the shape [gbrain](https://github.com/garrytan/gbrain) imports when you graduate to stage 2 — the migration becomes `gbrain init` + import, nothing to restructure.

## What lives where

| Path | Contents | Template |
| --- | --- | --- |
| `company.md` | What we sell, to whom, stage, priorities, how decisions get made | filled at install |
| `offers.md` | Products/offers, pricing, current state | filled at install |
| `customers/` | One page per customer/user: who, status, history, open items | `customers/_template.md` |
| `people/` | One page per team member, advisor, key contact | `people/_template.md` |
| `decisions/` | One page per decision: what, why, owner, revisit-when. Append-only history. | `decisions/_template.md` |
| `meetings/` | One page per meeting: decisions, commitments, open questions | `meetings/_template.md` |

## Hygiene rules

- **Honest gaps beat confident blanks:** when something is unknown, write `GAP: <what we don't know>` — agents must surface gaps instead of guessing.
- **Update on contact:** after any session that learns something about an entity, update its page (and say so in the page's log line).
- **Stale flag:** any page untouched for 6+ weeks that an agent relies on should be verified before trusting — the weekly staleness sweep (see `dream/CRONS.md`) flags these.
