# Migration: Flat-4+ to F4A Profiles

## Decision

F4A is now the governing method. Flat-4+ is retained as a legacy layer convention within the Hardware / Realtime Profile rather than the universal structure for every product.

## Mapping

| Previous concept | New position |
| --- | --- |
| L0–L4 and Utils dependency rules | Hardware / Realtime Profile, optional legacy convention |
| CQRS `L1 -> L4` fast-track | Removed from F4A Core; SaaS uses explicit query/application boundaries, legacy Flat-4 requires semantic review |
| Zero-GC and zero-copy | Optional hardware performance contract |
| `<16ms`, `<48°C`, `100Hz` | Product-specific measured thresholds |
| AI Pass@1 `>85%` | Optional experiment target with maintained dataset and baseline |
| Static layer scanner | Hardware Profile dependency-screening aid |
| ADR, tests, evidence | F4A Core |

## Migration rules

1. Identify deployable subsystems.
2. Assign one Primary Profile to each subsystem.
3. Keep existing layer structure when it is useful; do not reorganize solely for naming compliance.
4. Move numeric constraints into the owning product specification.
5. Mark unsupported performance claims as hypotheses until measured.
6. Retain historical ADRs but update their scope and evidence status.
