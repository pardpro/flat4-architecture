# F4A Core Governance

F4A Core governs how product intent becomes verifiable work. It does not prescribe one directory tree or universal layer model.

## Core cycle

| Stage | Required question | Durable evidence |
| --- | --- | --- |
| Frame | Who has what problem, what outcome matters, and what is explicitly out of scope? | Brief, issue, or equivalent intent record |
| Formalize | What behavior, boundary, permission, failure, and acceptance conditions apply? | Specification or acceptance criteria |
| Architect | What are the system, deployment, data, and trust boundaries? | Boundary description or diagram |
| Decide | Which costly or hard-to-reverse choice was made, and why? | ADR or equivalent decision record |
| Implement | What is the smallest coherent change and its completion condition? | Task, change set, or pull request record |
| Verify | What evidence demonstrates function, safety, security, and regression control? | Tests, CI, review, telemetry, or manual evidence |
| Learn | What happened, which assumption changed, and what debt remains? | Release note, incident review, metric review, or retrospective |

The evidence carrier is flexible. Use repository-native formats such as `AGENTS.md`, issues, specifications, C4-style diagrams, ADRs, tests, CI reports, or observability records.

## Risk-proportionate evidence

Classify a change by its highest applicable risk:

| Risk | Typical scope | Minimum evidence |
| --- | --- | --- |
| Low | Copy, styling, isolated non-critical fix | Intent, diff, focused verification |
| Standard | Ordinary feature or workflow change | Acceptance criteria, failure/empty cases, tests, rollback note when state changes |
| High | Auth, billing, personal data, migrations, AI actions, cross-module change | Threat/permission review, architecture boundary, ADR when consequential, migration and rollback evidence, observability |
| Critical | Safety, device control, irreversible action, regulated data, production infrastructure | Formal specification, independent review, controlled environment evidence, explicit authorization and recovery plan |

Do not inflate low-risk work into a documentation exercise. Do not downgrade risk to avoid evidence.

## Shared invariants

- Keep product intent and non-goals explicit.
- Make trust, data, deployment, and external-service boundaries visible.
- Treat AI output as untrusted until validated by deterministic rules and permissions.
- Preserve user authority before external or irreversible actions.
- Keep changes narrow enough to review and roll back.
- Verify more than the happy path when the risk requires it.
- Distinguish measured evidence from hypotheses and architectural intent.
- Keep durable project knowledge in the repository or another maintained system, not only in chat history.
