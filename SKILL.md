---
name: f4a-engineering-governance
description: "Apply Pardpro F4A engineering governance when the user explicitly requests F4A, needs architecture Profile selection or risk-proportionate delivery evidence, or works in a repository that declares F4A. Route each deployable subsystem to one primary Profile instead of imposing one universal layer structure. Do not activate for ordinary coding, planning, or review that has no F4A governance context."
---

# F4A Engineering Governance

Turn product intent into verifiable outcomes without forcing one code structure onto every project.

## Start with Core

Read [references/core-governance.md](references/core-governance.md). Establish the problem, user, desired outcome, non-goals, deployable subsystem boundaries, change risk, minimum durable evidence, acceptance conditions, and rollback conditions.

Do not create every possible document for every change. Scale evidence with risk.

## Select one primary profile per deployable subsystem

Read [references/profile-selection.md](references/profile-selection.md), then load only the selected profile:

- Web products, APIs, subscriptions, teams, and business workflows: [references/saas-profile.md](references/saas-profile.md)
- Devices, protocols, polling, offline recovery, constrained resources, and realtime behavior: [references/hardware-realtime-profile.md](references/hardware-realtime-profile.md)
- Agentic workflows, tool use, approvals, memory, and evaluation: [references/ai-agent-profile.md](references/ai-agent-profile.md)
- Content pipelines, analytics, datasets, and publishing: [references/content-data-profile.md](references/content-data-profile.md)

A monorepo may use multiple profiles, but each independently deployed subsystem must declare one primary profile. Shared F4A Core rules apply across the repository.

## Work evidence-first

1. Frame the requested outcome and explicit non-goals.
2. Formalize behavior, boundaries, permissions, failure cases, and acceptance criteria.
3. Identify system and deployment boundaries before choosing code organization.
4. Record only decisions that are costly, risky, or difficult to reverse.
5. Keep each implementation task narrow and name its completion evidence.
6. Verify successful, empty, failure, permission, concurrency, and recovery paths as relevant.
7. Record observed results, unresolved risk, and follow-up learning.

Use `AGENTS.md`, ADRs, C4-style diagrams, specifications, tests, CI, and telemetry as possible carriers of evidence, not as mandatory brands or formats.

## Audit without overclaiming

- Preserve read-only scope when the user asks for review or a report.
- Separate confirmed findings, tool warnings, assumptions, and unverified risks.
- Do not claim that architecture eliminates AI errors, provides hard realtime behavior, or proves performance without measured evidence.
- For Hardware / Realtime projects using the legacy Flat-4 layer convention, run `scripts/validate_flat4.py <project-path>` as a dependency-screening aid. Read [references/flat4-layer-rules.md](references/flat4-layer-rules.md) first.
- Treat a clean static scan as supporting evidence only; it cannot prove semantics, query purity, lock freedom, memory allocation, latency, thermal behavior, or operating-system scheduling.

## Present the result

Lead with the selected subsystem and primary profile, risk level and required evidence, architecture or audit decision, verified evidence and remaining uncertainty, and smallest safe next action.
