# F4A Audit Checklist

## Audit order

1. Identify deployable subsystems and their declared primary profiles.
2. Confirm product intent, non-goals, and risk classification.
3. Compare specifications, decisions, implementation, tests, and runtime evidence.
4. Load only the profile checklist relevant to each subsystem.
5. Trace the main path and relevant failure, permission, concurrency, and recovery paths.
6. Report documentation drift as an evidence-chain failure.

## Core checks

- Intent and non-goals are explicit.
- Trust, data, deployment, and external-service boundaries are visible.
- The selected Profile matches the subsystem's runtime responsibility.
- The evidence depth matches the risk.
- AI output is validated before persistence or action.
- Important decisions and exceptions are durable and owned.
- Tests and runtime evidence support claims; unmeasured claims are labeled hypotheses.
- Rollback or recovery exists where state, money, safety, or availability is at risk.

## Severity

- **P0:** Active safety, security, destructive, financial, or irreversible risk.
- **P1:** Missing authority/control boundary, incorrect primary profile, unrecoverable state risk, or critical untested failure path.
- **P2:** Material evidence gap, architectural drift, weak isolation, or missing observability.
- **P3:** Documentation, naming, or maintainability issue with limited immediate impact.

## Finding format

Include severity, subsystem/profile, evidence, violated rule, consequence, smallest correction, and verification needed. Separate confirmed findings, tool warnings, assumptions, and unverified risks.
