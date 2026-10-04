# F4A Hardware / Realtime Profile

Use for devices, protocols, drivers, polling, continuous streams, offline recovery, constrained resources, or timing-sensitive control.

## Responsibilities

- Domain: pure state transitions, units, thresholds, invariants, and algorithms.
- Input / Protocol: decode and validate serial, Bluetooth, USB, sensor, or network input.
- Coordinator: own device sessions, state progression, retries, timeouts, and fault isolation.
- Runtime Pipeline: manage buffers, timers, queues, scheduling, and resource lifecycles.
- Infrastructure / Drivers: isolate OS, hardware, filesystem, network, and persistence effects.
- Presentation / Integration: expose UI, cloud APIs, alerts, or external consumers.

These are responsibility boundaries, not a mandatory number of top-level folders. Projects already using the legacy Flat-4 layer convention may keep it; read [flat4-layer-rules.md](flat4-layer-rules.md).

## Realtime levels

- **Best effort:** latency matters but occasional misses are acceptable.
- **Soft realtime:** deadlines are measured and misses degrade quality but not safety.
- **Hard realtime:** a missed deadline is unacceptable and requires suitable hardware, runtime/RTOS, scheduling analysis, and end-to-end evidence.

Architecture alone never proves realtime behavior.

## Optional performance contracts

Apply only when the product evidence justifies them: bounded allocation or zero-allocation hot paths, zero-copy buffers, lock avoidance, wake-up batching, event-driven synchronization, thermal or power backpressure, offline caching, deterministic reconnection, and watchdog-safe recovery.

Record thresholds such as latency, temperature, frequency, memory, and power in the product specification, not as universal F4A constants.

## Evidence

- protocol fixtures and malformed-input tests;
- state-machine transition and recovery tests;
- fault injection, disconnect, timeout, and restart evidence;
- profiler traces for allocation and locks where constrained;
- measured latency distributions, not a single average;
- thermal and power traces from the target environment;
- explicit limitations of desktop/mobile OS scheduling;
- hardware-in-the-loop or controlled bench testing when risk warrants it.
