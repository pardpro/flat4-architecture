# F4A — AI-Native Engineering Governance

F4A is Pardpro's engineering governance and evidence-chain system for turning product intent into verifiable software and hardware outcomes.

F4A does **not** impose one universal code structure. It combines specification-first delivery, explicit system boundaries, durable decisions, AI-agent rules, automated verification, and architecture Profiles selected for each deployable subsystem.

F4A originated as **Flat-4 Architecture**. The name is now retained as the product brand while the original layer model continues as an optional Hardware / Realtime convention.

## Model

```text
F4A Core
  Frame → Formalize → Architect → Decide → Implement → Verify → Learn

F4A Profiles
  SaaS / Web App
  Hardware / Realtime
  AI Agent
  Content / Data
```

Every repository shares F4A Core. Each independently deployed subsystem declares one Primary Profile. A monorepo may contain several Profiles, but one code unit should not obey two incompatible primary structures.

## Core principles

- Make product intent and non-goals explicit.
- Scale evidence with risk instead of generating documentation mechanically.
- Make trust, data, deployment, and external-service boundaries visible.
- Treat AI output as untrusted until schemas, permissions, and business rules validate it.
- Keep changes narrow, reviewable, verifiable, and recoverable.
- Separate measured evidence from hypotheses and architectural intent.
- Preserve durable knowledge outside chat history.

## Profiles

### SaaS / Web App

Use domain-oriented modules, explicit adapters, server-authoritative permissions, safe migrations, observability, and validated AI boundaries. Prefer a modular monolith until distribution is justified.

### Hardware / Realtime

Use explicit protocol, state, scheduling, resource, driver, and recovery boundaries. Legacy Flat-4 layers remain available as an optional convention. Realtime, thermal, power, lock-free, and zero-allocation claims require target-environment evidence.

### AI Agent

Separate intent, planning, tool execution, approval, memory, and verification. Apply least privilege, structured validation, bounded retries, provenance, and task-specific evaluations.

### Content / Data

Separate sources, ingestion, transformation, storage, analysis, and publication. Preserve provenance, schema versions, quality checks, lineage, and reprocessing or rollback paths.

## Repository contents

- [`SKILL.md`](SKILL.md): Codex Skill that selects risk and Profile before applying rules.
- [`references/`](references): F4A Core, Profile definitions, audit and acceptance guidance.
- [`docs/`](docs): Product templates, architecture map, test strategy, metrics, and historical decisions.
- [`scripts/validate_flat4.py`](scripts/validate_flat4.py): Optional static dependency screen for Hardware / Realtime projects using legacy Flat-4 layers.
- [`scripts/simulate_l4_microburst.py`](scripts/simulate_l4_microburst.py): Educational batching model, not target-system performance proof.

## Install the Skill

The install folder must be named `f4a-engineering-governance`.

### One project only

Extract the release archive into the target repository so the result is:

```text
<project>/.agents/skills/f4a-engineering-governance/
  SKILL.md
  agents/
  references/
  scripts/
```

Open that project in Codex and invoke:

```text
$f4a-engineering-governance
```

### Personal installation

Extract the same folder into:

```text
~/.agents/skills/f4a-engineering-governance/
```

Codex detects Skill changes automatically; restart Codex if it does not appear.

## Test and package

Run the repository checks:

```bash
python -m unittest discover -s tests -v
python scripts/package_release.py
```

The packaging command reads `VERSION` and creates a reproducible archive under `dist/`. Generated archives are intentionally not committed; publish them as release assets so source history and release artifacts stay separate.

## Important boundaries

- Architecture reduces error propagation; it does not eliminate AI mistakes.
- A static scan supports review; it does not certify semantic correctness.
- Software structure does not create hard realtime guarantees or bypass operating-system scheduling.
- Numeric thresholds belong to product specifications and measured acceptance evidence, not universal F4A rules.

## 中文简介

F4A 是 Pardpro 面向 AI 辅助研发的工程治理与证据链体系，用于把产品意图转化为可验证的软件与硬件成果。

F4A 不强制所有项目采用同一代码分层。所有项目共享 F4A Core；每个可独立部署的子系统根据运行责任选择一个 Primary Profile：SaaS、Hardware / Realtime、AI Agent 或 Content / Data。

F4A 的核心不是“目录必须长什么样”，而是确保需求、边界、关键决策、实现范围、验证证据和复盘能够被人和 AI 持续理解。原有 Flat-4 严格分层被保留为 Hardware / Realtime Profile 的可选实现，而不再作为所有 SaaS 的通用宪法。

F4A 起源于 Flat-4 Architecture。现在 F4A 作为产品品牌继续使用，而最初的 Flat-4 分层成为 Hardware / Realtime Profile 下的可选约定。

安装时，将发行包中的 `f4a-engineering-governance` 文件夹完整解压到项目的 `.agents/skills/`，或个人目录的 `~/.agents/skills/`，然后在 Codex 中调用 `$f4a-engineering-governance`。

## License

MIT © 2026 PARDPRO TECHNOLOGIES LTD.
