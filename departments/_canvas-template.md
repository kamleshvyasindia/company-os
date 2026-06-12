# Workflow: [name]

- **Department:** [marketing / product / support / sales / ops]
- **DRI (named human):** [[people/...]]
- **Status:** [draft / live / paused / retired] — installed YYYY-MM-DD

## Sensor (trigger / cadence)
[what starts a run: an event ("new message in #feedback"), or a schedule ("every Friday 9:00")]

## Policy (the rules)
[what to do, what never to do, thresholds, tone. The judgment, written down.]

## Inputs
[exact sources: Slack channels, Linear views, brain pages, inbox patterns]

## Tools
[what it may call, at what tier — must match tools/registry.md. Extra write permissions granted here, narrowly.]

## Output artifact
[what a run produces, and where it lands (departments/<d>/outputs/...)]

## Quality gate
[checklist in reviews/ this output must pass BEFORE a human sees it. Every gate decision → logs/gate-failures.md]

## May do without asking / must ask first
[per-workflow deltas from rules.md — narrower only]

## Learning (write-back)
[what gets recorded after each run: outcome, what the gate caught, brain pages updated]

## Retire / revise when
[the condition that makes this workflow stale — e.g., "offer changes", "gate failure rate >30%"]
