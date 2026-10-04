# Pardpro F4A Acceptance Standard

Acceptance combines F4A Core evidence with the selected Profile and product-specific thresholds.

## Required record

- subsystem and primary Profile;
- change risk level;
- build/version and environment;
- intent, non-goals, and acceptance criteria;
- automated and manual evidence;
- security, privacy, permission, migration, recovery, or hardware evidence as applicable;
- expected and actual result;
- unresolved risk, owner, and follow-up;
- pass, conditional pass, or fail.

## Rules

- Do not accept a release solely because a static scanner, build, or happy-path test passes.
- Do not require hardware metrics for SaaS or content systems unless the product has those constraints.
- Do not claim AI quality, latency, thermal, power, lock freedom, or allocation behavior without a documented method and measured evidence.
- Conditional acceptance must name the limitation, owner, deadline, and containment.
