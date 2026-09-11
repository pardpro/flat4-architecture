# Pardpro Flat-4+ Architecture Rules

## Legal Call Paths
- **Write/Complex Flow**: `L1 -> L2 -> [L0, L3, L4, Utils]`
- **Read/Simple Query (CQRS)**: `L1 -> L4`

## Layer Responsibilities

### L0 Domain
- House pure business logic, mathematical algorithms, and core data structures.
- Do not perform any I/O, external network requests, or database accesses.

### L1 Entry
- Initialize runtime and serve as the single interface point.
- Route write requests to L2; read requests directly to L4.

### L2 Coordinator
- Act as the state machine holding task Context.
- Conform to the **Zero-GC Contract**: Pre-allocate the Memory Arena. Avoid `new`/`malloc` in high-frequency event loops.
- Handle thermal/power management strategy decisions (e.g. Backpressure) based on L4 signals.
- Never call another L2 directly.

### L3 Molecular (Optional)
- Combine L4 actions into reusable, zero-copy, stateless pipelines.
- Strictly forbid any Mutex or threading locks to ensure sub-millisecond data flow.
- Never call L1, L2, L0, or another L3.

### L4 Atomic
- Isolate all side-effects (Database, Network, OS Hardware Polling).
- Contain all debounced micro-burst mechanisms to prevent OS Watchdog kills.
- Never call L1, L2, L3, L4, or L0 (only Utils).

### Utils (Common)
- General-purpose tech functions (e.g. date parsers, string formatting) shared across all layers.

## Dependency Matrix

| Caller | May call | Must not call |
| --- | --- | --- |
| L1 | L2, L4 (Query only), Utils | L1, L3, L0 |
| L2 | L3, L4, L0, Utils, Policies | L1, L2 |
| L3 | L4, Utils | L1, L2, L3, L0 |
| L4 | Utils | L1, L2, L3, L4, L0 |
| L0 | Utils | L1, L2, L3, L4, L0 |
| Utils | Utils | L0, L1, L2, L3, L4 |

## Validation
All rules are strictly enforced by the included Python script equipped with a Deep AST (Abstract Syntax Tree) Parsing engine. Check `06_Evaluation_Metrics.md` for associated performance and AI-viability benchmarks.
