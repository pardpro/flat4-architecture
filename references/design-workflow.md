# F4A Delivery Workflow

## 1. Frame

State the user, problem, desired outcome, non-goals, and constraints. Identify the smallest independently valuable change.

## 2. Select boundaries and profile

List deployable subsystems and choose one primary F4A Profile for each. Record trust, data, external-service, and operational boundaries.

## 3. Classify risk

Use the highest relevant level from [core-governance.md](core-governance.md). Scale the required evidence accordingly.

## 4. Formalize behavior

Define inputs, outputs, permissions, state changes, failure/empty conditions, concurrency, recovery, and acceptance criteria relevant to the profile and risk.

## 5. Decide only what matters

Create an ADR for consequential or costly-to-reverse choices. Include context, considered alternatives, decision, consequences, evidence needed, and reconsideration trigger.

## 6. Implement narrowly

Break work into reviewable units. Keep domain decisions and external effects behind explicit boundaries appropriate to the selected Profile. Do not perform unrelated refactors.

## 7. Verify and learn

Collect proportionate automated and manual evidence. Record remaining uncertainty, observed metrics, rollback readiness, and lessons that should alter future work.
