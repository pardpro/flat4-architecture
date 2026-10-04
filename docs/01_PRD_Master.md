# F4A Product Brief & Specification Template

**Project / Subsystem:** [Name]
**Primary Profile:** [SaaS | Hardware / Realtime | AI Agent | Content / Data]
**Risk:** [Low | Standard | High | Critical]
**Status:** [Draft | Approved]
**Owner:** [Owner]

## 1. Frame

- **User / Operator:** Who experiences the problem?
- **Problem:** What is the current pain point and supporting evidence?
- **Outcome:** What observable result defines success?
- **Non-goals:** What is explicitly out of scope?

## 2. Boundaries

- **Deployment boundary:** How is this subsystem deployed and operated independently?
- **Trust boundary:** Which inputs, users, or services are untrusted?
- **Data boundary:** What data is processed, who owns it, and how long is it retained?
- **External systems:** Which databases, payment systems, AI services, devices, or third parties are involved?

## 3. Behavior

Describe the main path and the relevant empty, failure, permission, concurrency, timeout, retry, recovery, and rollback behavior.

## 4. Acceptance

Use observable conditions. Avoid unmeasurable terms such as "works normally," "fast," or "intelligent."

- [ ] [Success condition]
- [ ] [Failure / empty-state condition]
- [ ] [Permission / security condition]
- [ ] [Recovery / rollback condition]
- [ ] [Product-specific metric and measurement method]

## 5. Evidence plan

List the tests, reviews, telemetry, migration evidence, hardware bench evidence, or manual acceptance evidence required by the risk level.
