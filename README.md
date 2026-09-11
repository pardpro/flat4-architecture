# Pardpro's Flat-4 (Flat-4+) Architecture 🚀

<div align="center">
  <b>Built with ❤️ by <a href="https://pardpro.ca">PARDPRO TECHNOLOGIES LTD.</a></b><br>
  <i>The next-generation architecture designed specifically for AI-code generation and extreme hardware constraints.</i>
</div>

[English](#english) | [中文](#chinese)

---

<a id="english"></a>
## 🇬🇧 English

### What is Flat-4 Architecture?
Pardpro's Flat-4 is an incredibly strict, highly-deterministic software architecture pattern designed to eliminate "spaghetti code", cyclic dependencies, and unclear responsibilities. 

The enhanced **Flat-4+** version introduces Domain-Driven Design (DDD) concepts and Command Query Responsibility Segregation (CQRS) to balance strictness with development efficiency.

### Core Architecture Layers
The architecture is divided into the following strictly governed layers:
1. **L0 (Domain Layer)**: Pure data structures, entities, and business algorithms. No I/O, network, or DB calls allowed.
2. **L1 (Entry Layer)**: The entry point (e.g., API Controllers, CLI commands). Responsible for request parsing and environment setup. No business logic allowed.
3. **L2 (Coordinator Layer)**: The heart of the application. Owns the task Context, business decisions, branches, and orchestrates L0, L3, and L4.
4. **L3 (Molecular Layer)**: (Optional) Stateless sequences of tightly related L4 operations. No product-level policy branching.
5. **L4 (Atomic Layer)**: Single, isolated side-effects or I/O operations (e.g., DB queries, network requests).
6. **Utils (Common Layer)**: Pure technical functions (e.g., date formatting) accessible by all layers.

### The Ironclad Dependency Rules
- **No Same-Layer Calls**: L2 cannot call L2, L4 cannot call L4.
- **No Reverse Calls**: A lower layer (e.g., L4) can never call a higher layer (e.g., L2).
- **CQRS Fast-Track**: L1 must route through L2 for Writes (Commands), but may call L4 directly for simple Reads (Queries).

### Advanced Hardware & Performance Contracts (SR&ED Approved)
- **Zero-GC Memory Arena**: For >100Hz real-time systems, dynamic memory allocation (`new`/`malloc`) is strictly forbidden inside the L2 event loop. L1 must pre-allocate an Arena, and L2/L3/L4 must utilize strictly zero-copy, in-place mutation to eliminate GC pauses.
- **L4 Microsecond Isolation**: All interactions circumventing OS power policies (like App Nap/Modern Standby) via debounced micro-bursts must be strictly jailed within L4.

| Caller | May call | Must not call |
| --- | --- | --- |
| L1 | L2, L4 (Query only), Utils | L1, L3, L0 |
| L2 | L3, L4, L0, Utils, Policies | L1, L2 |
| L3 | L4, Utils | L1, L2, L3, L0 |
| L4 | Utils | L1, L2, L3, L4, L0 |
| L0 | Utils | L1, L2, L3, L4, L0 |
| Utils | Utils | L0, L1, L2, L3, L4 |

### 🌟 When to use Flat-4+ (The God-Tier Fit)
- **Hardware Integration, IoT, & Robotics**: When you need to isolate hardware polling, thermal limits, and erratic OS sleep behaviors from business logic.
- **AI-Native Code Generation**: Flat-4 is heavily deterministic. It provides AI agents (Cursor, Claude) with confined contexts, boosting first-pass (Pass@1) generation success rates to >85%.
- **Complex Domain & Financial Systems**: When you must strictly isolate the core algorithm (L0) from databases and network I/O.

### ❌ When NOT to use Flat-4+ (The Anti-Patterns)
- **Simple CRUD Websites**: If you are building a straightforward data-entry website, standard MVC (e.g., Django, Rails, Next.js) is significantly faster. Flat-4+ will introduce unnecessary boilerplate.
- **Pure Frontend/UI Development**: Modern UI libraries (React, Vue, SwiftUI) rely on declarative component trees. Forcing Flat-4's L1-L4 layers into UI rendering is an anti-pattern.
- **One-off Scripts or Big Data Pipelines**: Data engineering pipelines (Spark, Hadoop) rely on map-reduce and functional chains, not L2 state orchestrators.

### How to Use This Repository

This repository acts as an **AI Agent Skill / Architecture Toolkit**.

1. **For AI Agents (Cursor, Claude, Gemini, etc.)**: 
   Load the `SKILL.md` file into your AI assistant. The AI will then act as your strict Flat-4 Architect, helping you design code, refactor existing code, and generate Architecture maps.
2. **For Automated Auditing (AST-based)**:
   Use the Python static scanner to enforce the rules in your CI/CD pipeline. The tool now features a **Deep AST (Abstract Syntax Tree) Parsing** engine for Python source code, offering compiler-level dependency validation rather than basic regex matching.
   ```bash
   python scripts/validate_flat4.py /path/to/your/project
   ```
3. **For Manual Code Review**:
   Check the `references/` directory for detailed design workflows, architecture rules, and audit checklists.
4. **For Architecture Evaluation & SR&ED Compliance**:
   Refer to [`docs/06_Evaluation_Metrics.md`](docs/06_Evaluation_Metrics.md) to benchmark AI Pass@1 success rates and hardware CPU wake-up metrics. You can run the included simulation proof-of-concept:
   ```bash
   python scripts/simulate_l4_microburst.py
   ```

---

<a id="chinese"></a>
## 🇨🇳 中文

### 什么是 Flat-4 架构？
Pardpro's Flat-4 是一种极其严格、高度确定性的软件架构模式，旨在彻底消除“面条代码”、循环依赖以及职责不清的问题。

增强版的 **Flat-4+** 引入了领域驱动设计 (DDD) 的纯函数概念和 CQRS (命令查询职责分离)，在保持严格防腐的同时，兼顾了日常开发的效率。

### 核心架构分层
代码被严格划分为以下层级：
1. **L0 (Domain 领域层)**: 纯数据结构、实体和业务算法。绝对禁止任何 I/O、网络或数据库调用。
2. **L1 (Entry 入口层)**: 系统的入口（如 API Controller、CLI 命令）。只负责请求解析和环境初始化，禁止包含业务逻辑。
3. **L2 (Coordinator 协调层)**: 业务的心脏。持有任务上下文 (Context)，负责分支决策、状态流转，并负责编排 L0、L3 和 L4。
4. **L3 (Molecular 组合层)**: (可选) 无状态的、可复用的 L4 操作序列。不能包含产品级的业务分支策略。
5. **L4 (Atomic 原子层)**: 单一的、隔离的外部副作用或 I/O 操作（如查库、发请求）。
6. **Utils (Common 通用层)**: 纯技术型工具函数（如日期格式化），所有层都可以调用。

### 铁律级别的依赖控制
- **禁止同层调用**: L2 绝对不能调用 L2，L4 绝对不能调用 L4。
- **禁止反向调用**: 底层（如 L4）绝对不能调用上层（如 L2）。
- **读写分离快速通道**: 修改数据的操作 (Write) 必须走 `L1 -> L2`；但简单的纯数据查询 (Read) 允许 `L1 -> L4` 直达。

### 高性能与硬件契约 (SR&ED 核心标准)
- **零 GC 内存竞技场 (Zero-GC Arena)**：针对 >100Hz 的实时硬核业务，架构强制规定在 L2 的高频事件循环中**绝对禁止动态内存分配**（如 `new`/`malloc`）。L1 必须在启动时预分配对象池 (Arena)，L2~L4 必须采用零拷贝 (Zero-Copy) 与原地内存覆盖技术，彻底消除垃圾回收停顿。
- **L4 微秒级物理隔离**：对抗操作系统休眠惩罚（App Nap / Modern Standby）的微秒级轮询与防抖突发机制，必须被死死隔离在 L4 内，绝不污染上层业务循环。

| 调用方 | 允许调用 | 严禁调用 |
| --- | --- | --- |
| L1 | L2, L4 (仅限查询), Utils | L1, L3, L0 |
| L2 | L3, L4, L0, Utils, Policies | L1, L2 |
| L3 | L4, Utils | L1, L2, L3, L0 |
| L4 | Utils | L1, L2, L3, L4, L0 |
| L0 | Utils | L1, L2, L3, L4, L0 |
| Utils | 同层其他 Utils | L0, L1, L2, L3, L4 |

### 🌟 最佳适用场景 (神级契合)
- **软硬件结合项目（IoT、机器人、边缘计算）**：极其适合需要处理硬件轮询、对抗 OS 休眠、并有严苛散热和延迟要求（<16ms）的硬核设备。
- **AI 辅助编程 (AI-Native)**：Flat-4+ 规矩极其严格，能将大语言模型 (LLM) 的上下文收敛到极致。它能让 AI 的首发代码通过率 (Pass@1) 达到 85% 以上，绝不产生幻觉。
- **复杂的纯业务/科学计算系统**：L0 层能将最核心、最值钱的算法逻辑死死保护起来，隔绝一切网络和数据库的脏水。

### ❌ 适用反面教材 (杀鸡用牛刀)
- **普通的 CRUD 网站 / 后台管理**：如果你只是做个填表单存数据库的系统，用常规的 MVC（如 Django, Next.js）会快得多，强上 Flat-4+ 纯属增加样板代码。
- **纯前端/UI 界面开发**：React, Vue, SwiftUI 等讲究的是“声明式组件树”。把 Flat-4 强行套用在前端纯视图渲染上是非常别扭的，请放过它。
- **一次性的数据处理脚本或大数据管线**：大数据流（如 Spark）讲究 Map-Reduce 和函数式流，不需要 L2 这种重度状态机来做编排。

### 如何使用本工具包

这个仓库是一个完整的 **AI Agent 架构师技能包** 和 **静态审计工具**。

1. **让 AI 成为你的架构师**：
   在你的 AI 开发助手（如 Cursor, Claude, Gemini）中加载或复制 `SKILL.md` 的内容。AI 会自动掌握 Flat-4+ 的精髓，帮你从零设计模块、重构旧代码、生成架构图。
2. **自动化代码审计与编译级检测 (CI/CD)**：
   使用提供的 Python 脚本进行依赖扫描。该脚本内建了 **AST (抽象语法树) 解析引擎**，面对 Python 等项目时，能像真正的编译器一样精准定位跨层函数调用和导入，而非简单的正则表达式。
   ```bash
   python scripts/validate_flat4.py /path/to/your/project
   ```
3. **人工 Code Review 参考**：
   阅读 `references/` 目录下的设计工作流 (`design-workflow.md`) 和人工审计清单 (`audit-checklist.md`)，用于规范团队的代码审查标准。
4. **架构跑分与 SR&ED 评估标准**：
   参考 [`docs/06_Evaluation_Metrics.md`](docs/06_Evaluation_Metrics.md) 查看如何评估“AI 首次生成通过率”以及“操作系统唤醒/防抖效能”。你也可以直接运行以下概念验证 (PoC) 模拟器：
   ```bash
   python scripts/simulate_l4_microburst.py
   ```
