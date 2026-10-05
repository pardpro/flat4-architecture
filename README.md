# F4A — AI-Native Engineering Governance

[![Quality](https://github.com/pardpro/flat4-architecture/actions/workflows/quality.yml/badge.svg)](https://github.com/pardpro/flat4-architecture/actions/workflows/quality.yml)
[![Version](https://img.shields.io/badge/version-0.2.2-2563eb)](VERSION)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)
[![CI: Python 3.11](https://img.shields.io/badge/CI-Python%203.11-3776ab?logo=python&logoColor=white)](.github/workflows/quality.yml)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827)](SKILL.md)

**F4A is Pardpro's engineering governance and evidence-chain method for AI-assisted development. It helps teams turn product intent into reviewable, verifiable, and recoverable software and hardware outcomes.**

[English](#english) · [中文](#中文)

---

## English

> F4A does not force every project into one code structure. It provides a shared governance Core and selects an architecture Profile according to product risk and operating environment.

### Why F4A

AI can generate code quickly, but speed alone does not prove that requirements are correct, permissions are safe, data is trustworthy, or a release is recoverable. F4A makes these decisions durable inside the project so a team can answer:

- What problem are we solving, and what is explicitly out of scope?
- Where are the system, permission, and external-service boundaries?
- What level of evidence does this change require?
- Which results are verified, and which remain assumptions?
- How do we roll back and learn when something goes wrong?

### Operating model

```text
F4A Core
  Frame → Formalize → Architect → Decide → Implement → Verify → Learn

F4A Profiles
  SaaS / Web App
  Hardware / Realtime
  AI Agent
  Content / Data
```

Every repository shares F4A Core. Each independently deployable subsystem selects one Primary Profile. A monorepo may contain multiple Profiles, but one code unit should not follow two incompatible primary structures.

### The four Profiles

| Profile | Typical use | Governance focus |
| --- | --- | --- |
| SaaS / Web App | Web products, APIs, subscriptions, team workflows | Domain boundaries, server-authoritative permissions, safe migrations, observability, and validated AI inputs and outputs |
| Hardware / Realtime | Devices, protocols, polling, offline recovery, constrained resources | State, scheduling, resources, drivers, recovery boundaries, and target-environment evidence |
| AI Agent | Tool use, approvals, memory, automated tasks | Intent, planning, execution, permissions, validation, retries, provenance, and evaluation |
| Content / Data | Content pipelines, analytics, datasets, publishing | Sources, ingestion, transformation, storage, lineage, quality, and reprocessing |

### Install the Skill

The installation folder must be named `f4a-engineering-governance`.

#### Use in one project

Download the Skill archive from [Releases](https://github.com/pardpro/flat4-architecture/releases) and extract it into the target project:

```text
<your-project>/.agents/skills/f4a-engineering-governance/
  SKILL.md
  agents/
  references/
  scripts/
```

Open that project in Codex and enter:

```text
$f4a-engineering-governance
```

#### Use in your personal environment

Extract the same folder into:

```text
~/.agents/skills/f4a-engineering-governance/
```

Codex normally detects Skill changes automatically. Restart Codex if the Skill does not appear.

### How to use it

You do not need to be an architecture expert. Ask Codex in natural language:

```text
Use $f4a-engineering-governance to evaluate which Profile this project needs
and propose the minimum governance appropriate to its risk. Do not modify code yet.
```

You can also ask it to carry out the work:

```text
Use $f4a-engineering-governance to examine the system boundaries,
acceptance evidence, and rollback conditions for this change,
then implement and verify it according to the findings.
```

F4A identifies the subsystem and risk first, then loads only the required Profile. It does not mechanically generate every possible document for every project.

### Repository contents

- [`SKILL.md`](SKILL.md): Skill entry point for risk assessment and Profile selection.
- [`references/`](references): F4A Core, Profile, audit, and acceptance guidance.
- [`docs/`](docs): Product documentation, architecture map, test strategy, metrics, and historical decisions.
- [`scripts/hardware_realtime/validate_flat4.py`](scripts/hardware_realtime/validate_flat4.py): Optional static dependency checker for projects using the legacy Flat-4 layer convention.
- [`scripts/hardware_realtime/simulate_l4_microburst.py`](scripts/hardware_realtime/simulate_l4_microburst.py): Educational batching model; it is not proof of target-device performance.
- [`tests/`](tests): Tests for language policy, the dependency checker, the simulator, and release packaging.

### Verify and package

GitHub Actions automatically runs the documentation policy check and unit tests. Run the same checks locally with:

```bash
python scripts/check_english_docs.py
ruff check .
python -m unittest discover -s tests -v
python scripts/package_release.py
```

The packaging script reads [`VERSION`](VERSION) and creates a reproducible Skill archive plus a SHA-256 checksum under `dist/`. Generated artifacts are excluded from Git history and should be published as GitHub Release assets.

### Important boundaries

- Architecture can reduce error propagation; it cannot eliminate AI mistakes.
- Static analysis can support review; it cannot prove business semantics.
- Software layering cannot create hard realtime guarantees or bypass operating-system scheduling.
- Numeric thresholds must come from product specifications and measured evidence, not universal F4A rules.

---

## 中文

**F4A 是 Pardpro 面向 AI 协作开发的工程治理与证据链方法。它帮助团队把产品意图转化为可审查、可验证、可恢复的软件与硬件成果。**

> F4A 不要求所有项目采用同一种代码结构。它提供一套共同的治理核心，并根据产品风险与运行环境选择合适的架构 Profile。

### 为什么需要 F4A

AI 可以快速生成代码，但速度本身不能证明需求正确、权限安全、数据可信或发布可恢复。F4A 把这些关键判断固化到项目中，让团队能够回答：

- 我们正在解决什么问题，明确不做什么？
- 系统边界、权限边界和外部服务边界在哪里？
- 这项改动需要什么级别的证据？
- 哪些结果已经验证，哪些仍是假设？
- 出现问题时如何回滚和继续学习？

### 工作模型

```text
F4A Core
  Frame → Formalize → Architect → Decide → Implement → Verify → Learn

F4A Profiles
  SaaS / Web App
  Hardware / Realtime
  AI Agent
  Content / Data
```

每个仓库共用 F4A Core。每个可独立部署的子系统选择一个主要 Profile。同一个 monorepo 可以包含多个 Profile，但一个代码单元不应同时服从两套互相冲突的主要结构。

### 四种 Profile

| Profile | 适用场景 | 重点治理内容 |
| --- | --- | --- |
| SaaS / Web App | Web 产品、API、订阅、团队工作流 | 领域边界、服务端权威权限、安全迁移、可观测性、AI 输入输出验证 |
| Hardware / Realtime | 设备、协议、轮询、离线恢复、受限资源 | 状态、调度、资源、驱动、恢复边界与目标环境证据 |
| AI Agent | 工具调用、审批、记忆、自动化任务 | 意图、规划、执行、权限、验证、重试、来源与评估 |
| Content / Data | 内容管线、分析、数据集、发布 | 来源、摄取、转换、存储、血缘、质量与重新处理能力 |

### 安装 Skill

安装目录必须命名为 `f4a-engineering-governance`。

#### 仅在一个项目中使用

下载 [Releases](https://github.com/pardpro/flat4-architecture/releases) 中的 Skill 压缩包，解压到目标项目：

```text
<你的项目>/.agents/skills/f4a-engineering-governance/
  SKILL.md
  agents/
  references/
  scripts/
```

然后在 Codex 中打开该项目并输入：

```text
$f4a-engineering-governance
```

#### 在个人环境中使用

将同一个文件夹解压到：

```text
~/.agents/skills/f4a-engineering-governance/
```

Codex 通常会自动识别 Skill 变化。如果没有出现，请重启 Codex 后再检查。

### 如何使用

你不需要先成为架构专家。可以直接用自然语言告诉 Codex：

```text
请使用 $f4a-engineering-governance，评估这个项目应选择哪个 Profile，
并给出与风险相匹配的最小治理方案。先不要修改代码。
```

也可以要求它执行具体工作：

```text
请使用 $f4a-engineering-governance 检查这个改动的系统边界、
验收证据和回滚条件，然后按结论完成实现与验证。
```

F4A 会先识别子系统和风险，再加载所需 Profile。它不会机械地为每个项目生成全部文档。

### 仓库结构

- [`SKILL.md`](SKILL.md)：Skill 入口，负责风险判断与 Profile 选择。
- [`references/`](references)：F4A Core、Profile、审计与验收规则。
- [`docs/`](docs)：产品说明、架构图、测试策略、指标和历史决策。
- [`scripts/hardware_realtime/validate_flat4.py`](scripts/hardware_realtime/validate_flat4.py)：面向旧版 Flat-4 分层项目的可选静态依赖检查器。
- [`scripts/hardware_realtime/simulate_l4_microburst.py`](scripts/hardware_realtime/simulate_l4_microburst.py)：教学用途的批处理模型，不代表目标设备性能证明。
- [`tests/`](tests)：语言策略、依赖检查器、模拟器和发行打包测试。

### 验证与打包

本仓库通过 GitHub Actions 自动执行文档策略检查和单元测试。本地可运行：

```bash
python scripts/check_english_docs.py
ruff check .
python -m unittest discover -s tests -v
python scripts/package_release.py
```

打包脚本读取 [`VERSION`](VERSION)，在 `dist/` 中生成可复现的 Skill 压缩包及 SHA-256 校验文件。生成物不进入 Git 历史，应作为 GitHub Release 附件发布。

### 重要边界

- 架构可以降低错误传播，但不能消除 AI 错误。
- 静态扫描可以辅助审查，但不能证明业务语义正确。
- 软件分层不能凭空提供硬实时保证，也不能绕过操作系统调度。
- 数字阈值应来自具体产品规范和实测证据，而不是被写成通用 F4A 规则。

---

## License / 许可证

[MIT](LICENSE) © 2026 PARDPRO TECHNOLOGIES LTD.
