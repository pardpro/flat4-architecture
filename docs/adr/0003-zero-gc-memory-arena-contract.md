# ADR-003: Bounded-allocation hot paths for constrained runtimes

**Status:** Optional performance contract
**Scope:** Hardware / Realtime hot paths with demonstrated allocation or GC risk

## Context

Allocation and garbage collection can introduce latency variance in some managed runtimes. The impact depends on runtime, allocation rate, heap behavior, workload, and deadline. A universal Zero-GC mandate would add complexity to systems that do not need it.

## Decision

Use a bounded-allocation or zero-allocation contract only for identified hot paths when profiling shows it is necessary. Record the owning component, runtime, workload, budget, measurement method, and fallback behavior.

Preallocation, pooling, arenas, zero-copy buffers, or in-place mutation are implementation options rather than universal layer responsibilities.

## Consequences

- Ordinary SaaS and low-frequency code are not burdened with premature memory optimization.
- Constrained paths gain explicit budgets and repeatable evidence.
- Pools and arenas must address ownership, exhaustion, reuse, safety, and observability.

## Required evidence

- representative target-runtime profile;
- allocation and GC distribution under sustained load;
- latency distribution and deadline misses;
- exhaustion, overflow, and recovery tests.
