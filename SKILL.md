---
name: flat-4-plus-architect
description: "Design, implement, document, and audit software using the enhanced Pardpro's Flat-4+ architecture: L0 Domain, L1 Entry, L2 Coordinator, optional L3 Molecular, L4 Atomic, and Utils. Use when the user mentions Flat-4, Flat-4+, Pardpro architecture rules, CQRS fast-track, L0 domain modeling, layer dependency checks, architecture-map generation, or asks where code belongs. Also use when a repository declares it follows Flat-4/Flat-4+."
---

# Flat-4+ Architect

Apply the enhanced Pardpro's Flat-4+ architecture without forcing it onto unrelated projects. 

## Select the workflow

1. Determine whether the user wants design, implementation, documentation, or audit.
2. Preserve read-only scope when the user asks only for review or a report.
3. Read [references/architecture-rules.md](references/architecture-rules.md) and [docs/05_Flat4_Plus_Optimization.md](docs/05_Flat4_Plus_Optimization.md) before making placement or dependency decisions.
4. For new features or architecture documents, read [references/design-workflow.md](references/design-workflow.md).
5. For audits, read [references/audit-checklist.md](references/audit-checklist.md).
6. For acceptance planning, read [references/pard-acceptance.md](references/pard-acceptance.md).

## Work L2-first with L0 in mind

1. Describe the user-visible objective and constraints, explicitly including thermal limits, max latency (e.g., <16ms), and OS power-management barriers.
2. Write the L2 flow, Context, branches, errors, retries, and rollback decisions before implementation.
3. For core business logic and state transitions, define L0 (Domain) entities and pure functions. L2 should orchestrate calls to L0.
4. Extract shared business logic across L2s into Policies/Strategies and inject them.
5. Define every required L3/L4 interface with explicit input, output, and error behavior.
6. **Hardware & Performance Check**: For L3 interfaces, enforce stateless, lock-free pipelines to avoid GC and thread-locking in high-frequency streams. For L4, isolate OS microsecond polling and power states from main threads.
7. Use L3 only for a reusable, stateless sequence of tightly related L4 operations.
8. Implement or place code only after the flow and interfaces are clear.

## Audit with evidence

1. Inspect repository instructions and the actual directory structure.
2. Run `scripts/validate_flat4.py <project-path>` when the project is available locally (Note: verify script supports Flat-4+ rules).
3. Treat scanner findings as evidence, not proof; verify each reported dependency in source.
4. Check behavioral rules that static scanning cannot prove: especially Context ownership, L0 purity (no I/O), CQRS fast-track correctness, and orchestration inside L4.
5. Report confirmed violations separately from risks and optional improvements.
6. Do not modify files unless the user asks for changes.

## Preserve these Flat-4+ invariants

- **Command (Write) flows**: Allow `L1 -> L2 -> L4` and `L1 -> L2 -> L3 -> L4`.
- **Query (Read) fast-track**: Allow `L1 -> L4` exclusively for simple queries without business side-effects.
- **L0 Domain purity**: L0 must remain free of I/O, network, or external dependencies. It only performs pure memory computations.
- **Utils accessibility**: `Utils` can be called by any layer (L0-L4), but `Utils` cannot call L0-L4.
- Keep L3 optional and free of business-flow state.
- Keep task-level Context and business decisions in L2.
- Prohibit same-layer calls (except within Utils) and reverse calls.
- Permit external I/O in L4 when one atomic action is isolated and dependencies are explicit.

## Present results

- Lead with the architecture decision or ship/no-ship conclusion.
- Explain placement decisions in plain language (e.g., why a function belongs in L0 vs L4).
- For a violation, identify caller layer, target layer, violated rule, and smallest correction.
- State limitations when runtime behavior or dynamic imports prevent confirmation.
