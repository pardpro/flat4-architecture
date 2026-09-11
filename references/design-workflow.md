# Flat-4+ Design Workflow

## 1. Define Objective & Constraints
Record user-visible outcomes, and explicitly document extreme constraints (e.g., thermal thresholds <48°C, latency <16ms, OS sleep behaviors, AI Pass@1 targets).

## 2. Design Domain (L0) & Context
Define pure business data entities and pure mathematical algorithms in **L0 (Domain)**.
Define the pre-allocated Memory Arena schema that **L2** will hold to satisfy the Zero-GC contract.

## 3. Map the Flow (L2)
Write the L2 Coordinator state machine:
1. Receive request from **L1**.
2. Pre-allocate or reset Context Arena (No `new` inside loops).
3. Call **L4** atomic driver/API to fetch state.
4. Pass state to **L0** for pure logic evaluation.
5. Apply shared Policies (e.g., Thermal Backpressure dropping frames).
6. Pass results to **L3** stateless pipelines for zero-copy transmission.

## 4. Define L4 Side-Effects
Strictly isolate all I/O, database access, network calls, and OS microsecond polling into **L4**. Ensure L4 isolates main-thread wait states from the Coordinator loop.

## 5. Directory Layout
```text
src/
  L0_Domain/
  L1_Entry/
  L2_Coordinator/
  L3_Molecular/
  L4_Atomic/
  Utils/
```

## 6. Audit & Acceptance
Use the provided `validate_flat4.py` AST scanner. If the AST scan fails or the WPA micro-burst telemetry fails, the design is rejected.
