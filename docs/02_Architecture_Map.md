# F4A Architecture Map

## Governance and runtime relationship

```mermaid
flowchart TD
  C["F4A Core: intent, boundaries, decisions, evidence"] --> S["Deployable subsystem"]
  S --> P{"Select one Primary Profile"}
  P --> SaaS["SaaS / Web App"]
  P --> HW["Hardware / Realtime"]
  P --> Agent["AI Agent"]
  P --> Data["Content / Data"]
  SaaS --> E["Profile-specific implementation and evidence"]
  HW --> E
  Agent --> E
  Data --> E
```

## Subsystem inventory

| Subsystem | Deployment boundary | Primary Profile | Risk | External dependencies | Owner |
| --- | --- | --- | --- | --- | --- |
| [example-api] | [cloud service] | SaaS | High | DB, payment | [owner] |

## Contract map

For each connection between subsystems, record protocol, schema/version, authentication, timeout, retry/idempotency, failure behavior, and ownership.

## Rule

Profiles apply to deployable subsystems, not blindly to the repository root. Shared libraries must declare who owns their contracts and which subsystem may depend on them.
