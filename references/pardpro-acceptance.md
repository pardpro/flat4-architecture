# Pardpro Acceptance Standard (Flat-4+)

Use this as the company-level acceptance layer after automated tests and AST static analysis. Tailor concrete checks to the product instead of treating the examples as universal requirements.

## Architecture & Code Acceptance

- Confirm the codebase passes `python scripts/validate_flat4.py` via the **Deep AST Scan** without illegal cross-layer imports.
- Confirm **L0 (Domain)** remains mathematically pure and retains zero awareness of I/O.
- Confirm **L2 (Coordinator)** utilizes the pre-allocated Context Arena and contains no dynamic memory allocations (`new`, `malloc`) within high-frequency loops (Zero-GC Contract).
- Confirm **L4 (Atomic)** successfully hides all OS micro-burst/polling artifacts from the business layers.

## Hardware & SR&ED Performance Acceptance

- **Thermal Constraint**: Physical touch points remain <48°C during sustained load, enforced by L2 active frame dropping.
- **Micro-burst Efficiency**: CPU wake-up traces (WPA/Instruments) show at least an 80% reduction in erratic wake-ups; Watchdog kills are zero.
- **Latency Budget**: Event-driven L2 delta syncs maintain <16ms end-to-end turnaround.
- **AI Pass@1 Rate**: AI-assisted L4 additions must pass unit tests on the first generated prompt >85% of the time, proving extreme architecture decoupling.

## Release Record

Record build version, test scenario, thermal/profiling evidence (WPA traces), AI evaluation logs, and tester/date. Do not label a release as Pardpro-accepted unless both the AST validator and the hardware profiling confirm the architecture rules were not bypassed.
