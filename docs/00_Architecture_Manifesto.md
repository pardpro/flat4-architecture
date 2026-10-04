# F4A Engineering Governance Manifesto

## Why F4A exists

AI-assisted development increases implementation speed, but it can also amplify misunderstood requirements, cross-module coupling, missing failure paths, fragmented knowledge, and forgotten decisions. F4A does not aim to make AI infallible. It aims to expose errors earlier, reduce their blast radius, preserve decision history, and make outcomes verifiable.

## What F4A is

F4A is a governance and evidence chain from product intent to operational outcome:

1. **Frame:** Define the problem, user, desired outcome, and non-goals.
2. **Formalize:** Define behavior, boundaries, permissions, failure cases, and acceptance criteria.
3. **Architect:** Define system, deployment, data, and trust boundaries.
4. **Decide:** Record consequential and difficult-to-reverse choices.
5. **Implement:** Constrain each change and name its completion evidence.
6. **Verify:** Validate function, safety, recovery, and regression behavior.
7. **Learn:** Preserve observed metrics, changed assumptions, and technical debt.

F4A may use `AGENTS.md`, specifications, C4-style diagrams, ADRs, tests, CI, and telemetry as evidence carriers. It does not mandate a particular tool brand or a fixed number of documents.

## Profile principle

Different runtime environments need different code organizations and quality gates. SaaS systems should not be forced into hardware-oriented layers, and device systems should not be governed like ordinary CRUD applications. Each deployable subsystem therefore selects one Primary Profile while sharing F4A Core.

The original Flat-4 layer convention remains valuable, primarily within the Hardware / Realtime Profile. It can reduce dependency spread and improve the reviewability of state, protocol, and side effects. It does not automatically provide hard realtime behavior, zero defects, or error-free AI output.
