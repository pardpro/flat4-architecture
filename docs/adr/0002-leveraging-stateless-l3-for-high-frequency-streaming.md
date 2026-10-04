# ADR-002: Prefer stateless pipeline stages in high-frequency streams

**Status:** Profile-specific; conditional
**Scope:** Hardware / Realtime streams where state or lock contention is measured as a risk

## Context

High-frequency streams can suffer from allocation churn, queue growth, contention, and unclear ownership. Stateless transformations simplify testing and can reduce these risks, but buffers, framing, ordering, and recovery may still require owned state.

## Decision

Prefer stateless transformation stages. Place necessary state in an explicitly owned session, coordinator, buffer, or runtime component with defined lifecycle and concurrency rules. Do not ban locks or allocation globally; select mechanisms based on measured constraints and correctness requirements.

## Consequences

- Transformation logic remains easier to test and reuse.
- Stateful runtime concerns become visible rather than hidden inside utility code.
- Lock-free and zero-copy designs remain optional optimizations requiring profiling and correctness evidence.

## Required evidence

- throughput, latency distribution, allocation, and contention profile;
- ordering, backpressure, overflow, packet-loss, and recovery tests;
- proof that any lock-free structure is race-safe on the target runtime.
