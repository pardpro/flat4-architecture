# F4A Verification Plan

## Core verification

- Intent and non-goals match the delivered behavior.
- Acceptance criteria are observable and tested.
- Evidence depth matches the risk classification.
- Documentation and implementation describe the same boundaries.
- Rollback or recovery is verified when state or external actions are involved.

## SaaS Profile

- Success, empty, failure, permission, concurrency, and idempotency paths as relevant.
- Server-authoritative validation.
- Migration compatibility and rollback.
- External provider failure and rate-limit behavior.
- User-journey observability.

## Hardware / Realtime Profile

- Protocol fixtures and malformed input.
- State transitions, disconnect, timeout, restart, and recovery.
- Target-environment latency distribution and resource profiling when required.
- Thermal, power, allocation, and lock evidence only when specified.
- Hardware-in-the-loop for safety- or device-critical behavior.

## AI Agent Profile

- Schema validation, permissions, prompt injection, tool failure, bounded retry, duplicate action, stale memory, and partial completion.
- Task-specific evaluation dataset and regression baseline.

## Content / Data Profile

- Schema, data quality, missing/late input, reconciliation, lineage, retention, reprocessing, and publication approval.

Passing a build or static scanner is supporting evidence, not complete acceptance.
