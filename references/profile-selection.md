# F4A Profile Selection

Choose a profile for each independently deployable subsystem. A repository may contain several subsystems and therefore several profiles.

## Decision table

| Primary concern | Primary profile |
| --- | --- |
| Accounts, teams, permissions, billing, APIs, workflows, web applications | SaaS |
| Devices, protocols, polling, offline recovery, resource control, timing | Hardware / Realtime |
| Autonomous or semi-autonomous tool use, approvals, memory, evaluation | AI Agent |
| Ingestion, transformation, datasets, analytics, publishing, lineage | Content / Data |

Choose based on runtime responsibility, not the technology name. A web dashboard for a device fleet is normally SaaS; firmware and the local device service are Hardware / Realtime.

## Mixed systems

| Deployable subsystem | Primary profile |
| --- | --- |
| Embedded firmware | Hardware / Realtime |
| Desktop device service | Hardware / Realtime |
| Cloud API | SaaS |
| Web dashboard | SaaS |
| Support agent | AI Agent |
| Telemetry warehouse | Content / Data |

Define explicit contracts between subsystems. Do not make one code unit obey two incompatible primary structures. Secondary concerns become local constraints, not a second constitution.

## Selection record

Record subsystem name and deployment boundary, primary profile and reason, risk level, external systems and trust boundaries, measurable constraints, and exceptions with their owner.
