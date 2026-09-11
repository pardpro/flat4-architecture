# Flat-4 Audit Checklist

## Audit order

1. Read repository instructions, product requirements, architecture maps, and test plans.
2. Identify the actual naming convention for L1-L4.
3. Run the static validator when local source is available.
4. Verify every static finding in source before calling it confirmed.
5. Trace at least one normal flow and one failure flow end to end.
6. Compare documentation with implementation and report drift.

## Required checks

### L0 (Domain)
- Contains only pure data structures, algorithms, and business rules.
- Free of any external I/O, network, or DB calls.
- Does not call L1-L4.

### L1
- Calls L2 for commands/writes, or L4 for simple queries (CQRS Fast-Track).
- Can call Utils.
- Contains no domain branching, retry policy, rollback, or low-level operation.

### L2
- Owns the task Context and state transitions.
- Makes business decisions explicitly by orchestrating L0.
- Calls only L0, L3, L4, Utils, or injected Policies within the Flat-4 layers.
- Does not hide low-level computation or driver code.

### L3
- Exists only for a reusable standard composition.
- Calls only L4 and Utils.
- Does not retain Context or decide product policy.

### L4
- Has one clear operation and contract.
- Does not call another Flat-4 component (except Utils).
- Has no hidden mutable business state.
- Exposes external side effects and dependencies clearly.

### Utils / Common
- Strictly technical pure functions (e.g., date parsing, string formatting).
- Does not call L0, L1, L2, L3, or L4.

### Performance & Hardware Compliance (SR&ED Metrics)
- **L4 Hardware Isolation**: OS microsecond polling, power-saving circumventions (e.g., App Nap/Modern Standby), and debounced micro-burst mechanisms are strictly isolated within L4, preventing main-thread lockups.
- **L3 High-Frequency Streaming**: Inter-layer communication handling >100Hz telemetry avoids garbage collection (GC) churn and lock contention by adhering strictly to the L3 stateless rule.
- **L2 Thermal Profiling & Latency**: Event-driven delta sync inside L2 maintains an end-to-end latency budget of <16ms, while coordinating downstream CPU throttling/backlight modulation to guarantee touch-safe temperatures (<48°C).

### Tests and documentation

- L4 boundaries and external failures have tests.
- L2 normal, failure, retry, and rollback paths have tests.
- L1 has smoke coverage.
- Architecture documentation matches actual dependencies.
- Pardpro acceptance checks cover user-visible or hardware-dependent results.

## Severity

- **P0:** Safety violation, destructive behavior, or architecture breach that can corrupt state or bypass required control.
- **P1:** Confirmed reverse/same-layer dependency, business state outside L2, or missing critical failure flow.
- **P2:** Structural drift, weak test isolation, unnecessary L3, or ambiguous interface likely to cause defects.
- **P3:** Naming, documentation, or maintainability issue with limited immediate impact.

## Reporting format

For every finding, include:

- severity;
- evidence with file and line;
- caller and target layers;
- violated rule;
- practical consequence;
- smallest safe correction.

Separate confirmed findings from scanner warnings and unverified runtime risks. A clean scanner result does not prove architectural compliance because dynamic imports, dependency injection, and behavioral state require source review.
