# F4A Evaluation Metrics

F4A has no universal performance target. Each program defines a baseline, measurement method, sample size, environment, target, and decision threshold.

## Core governance metrics

- escaped defect rate and severity;
- change failure and rollback rate;
- lead time from approved intent to verified outcome;
- percentage of high-risk changes with required evidence;
- documentation/implementation drift findings;
- unresolved risk aging.

## AI-assisted development metrics

- task success on a maintained representative dataset;
- human correction rate;
- unsafe or unauthorized action rate;
- regression rate across model/prompt/tool changes;
- cost and latency per successful task;
- provenance and reproducibility of the evaluation.

Pass@1 may be measured for a defined task set, but no universal percentage proves architecture quality.

## SaaS metrics

Measure product-relevant reliability, authorization failures, workflow completion, provider errors, migration health, and user-impacting latency.

## Hardware / Realtime metrics

Measure target-device latency distributions, deadline misses, packet loss, recovery time, allocations, lock contention, CPU wake-ups, thermal behavior, and power only where the specification requires them.

The micro-burst script in this repository is an educational model. It does not replace WPA, Instruments, hardware-in-the-loop, or target-device evidence.
