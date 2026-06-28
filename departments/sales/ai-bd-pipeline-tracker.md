# Workflow: ai-bd-pipeline-tracker

- **Department:** sales
- **DRI (named human):** [[people/kamlesh.md]]
- **Status:** draft — installed 2026-06-28

> The first workflow loop for the sales department: tracking business development opportunities, focusing on the 90-day AI training goal (5 crores), and coordinating follow-ups and invoicing status with the team leaders.

## Sensor
Every Friday 15:00 — and ad-hoc when Kamlesh runs it.

## Policy
- Projections and estimates must never be assumed or predicted without checking with [[people/kamlesh.md]].
- Identify and flag any project that has been delayed in proposal submission or invoicing.
- Cross-check new accounts/projects against known independence constraints (Deloitte audit clients).
- Focus strictly on education-related BD. Skills-related work must be left out.
- Maintain a people-first tone, drafting reminder follow-ups for team leaders that are supportive and collaborative.

## Inputs
- `brain/company.md` (context & goals)
- `brain/offers.md` (positioning & pricing rules)
- `brain/customers/` pages (current client statuses: MoE Higher Ed, MoE School Ed/NCERT, Gujarat, Punjab, UP, Google, Manipal)
- `inbox/` capture logs (to scan for newly reported BD leads, meetings, or client feedback)

## Tools
GitHub / Git CLI (read/write to update customer pages and write pipeline logs), Local filesystem.

## Output artifact
`departments/sales/outputs/YYYY-MM-DD-sales-mis-pipeline-report.md`:
1. **AI BD Tracker**: Progress towards the 90-day 5 crores AI training business target, highlighting active proposals (e.g. Google, Manipal).
2. **Weekly MIS Summary**: Invoices raised, positions vacant, and proposal statuses per account.
3. **Draft Follow-ups**: Supportive and collaborative draft messages to team leaders (Priyank, Deependra, Meethi, Bhavisha, Arvind, Rajat, Deb) for pending invoices, proposals, or updates.
4. **Compliance Flags**: A check of active BD against Deloitte's audit independence rules.

## Quality gate
`reviews/sales-mis-checklist.md` — ensures all numbers are verified, no predictions are made without checking, and tone is supportive. Gate decisions → `logs/gate-failures.md`.

## May do without asking / must ask first
- May: Draft reports, update customer pipeline pages in the brain, draft follow-up templates.
- Must ask: Send any external/internal messages or finalize any MIS predictions.

## Learning (write-back)
- Update client/proposal status directly on `brain/customers/` pages.
- Log any gate failures or process delays to `logs/gate-failures.md`.

## Retire / revise when
The 90-day AI training target is met or changed, or the gate failure rate exceeds 30%.
