# ADR-001: Isolate OS power-management interactions at the hardware boundary

**Status:** Profile-specific; evidence required
**Scope:** Hardware / Realtime subsystems with background device communication

## Context

Desktop and mobile operating systems may throttle background work. Continuous polling can increase wake-ups and power use, while batching can increase latency. The correct balance depends on the target OS, device, transport, lifecycle, and product deadline.

## Decision

Keep OS scheduling, device polling, and power-management APIs behind the Hardware / Realtime infrastructure or driver boundary. Expose events, state, and explicit errors to the coordinator rather than leaking OS primitives into business logic.

Use event-driven behavior, batching, debounce, backoff, or keep-alive mechanisms only when supported by the platform and verified against the product specification.

## Consequences

- Business state remains testable without the target OS.
- Platform-specific behavior stays replaceable and observable.
- No claim is made that this boundary bypasses OS scheduling or prevents watchdog termination.

## Required evidence

- target OS/device and lifecycle conditions;
- latency and wake-up distributions;
- power or thermal trace when relevant;
- background/suspend/resume and failure-recovery tests.

Historical numeric claims are not universal F4A requirements and must be revalidated per product.
