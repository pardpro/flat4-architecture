# 架构评估标准 (Evaluation Metrics)

为了验证 Flat-4 架构在实际业务中的有效性，我们制定了以下两项核心量化考核指标。所有接入 Flat-4 的子项目，均须以该标准作为验收依据，确保架构动作没有变形。

## 1. 物理性能指标：OS 唤醒与防抖效能 (Micro-burst Efficiency)
- **定义**：在 100Hz 甚至更高的传感器数据流下，L4 层硬件轮询对操作系统（如 Windows Modern Standby / macOS App Nap）的唤醒干扰频率。
- **验证方法**：使用 Windows Performance Analyzer (WPA) 或 macOS Instruments，抓取 CPU C-State 切换日志。
- **基准线 (Baseline)**：
  - 传统模式：唤醒频次直接挂钩数据频率（例如 >100次/秒），导致 CPU 无法进入深度休眠，极易被 OS Watchdog 挂起或强杀。
  - **Flat-4 模式**：强制采用 L4 事件驱动和微突发滑动窗口 (Micro-burst window) 后，CPU 唤醒次数应严格降低至少 **80%**。且连续高压运行 1 小时，Watchdog 异常拦截次数必须为 **0**。
- **模拟验证工具**：可运行本仓库提供的 `python scripts/simulate_l4_microburst.py` 进行直观的 PoC 基准对比推演。

## 2. 软件工程指标：AI 一次性通过率 (AI Pass@1 Rate)
- **定义**：大语言模型 (LLM) 在给定产品需求和现有 Flat-4 接口文档下，单次生成的代码（无需人工进行二次 Bug 修复）即可直接通过单元测试并运行的概率。
- **验证方法**：参照 SWE-bench 评测方法论，在内部开发环节进行 A/B 统计。
- **基准线 (Baseline)**：
  - 传统 MVC/MVVM：受限于深层上下文污染和交织的副作用，大模型生成的代码经常出现幻觉，AI Pass@1 通常徘徊在 30%-40%。
  - **Flat-4 模式**：由于 L4 完全隔离了副作用，L0 隔离了 I/O，L3 保证了纯无状态，大模型需要的推理上下文极其收敛（填空式编程）。项目验收要求常规业务流的 AI Pass@1 必须稳定在 **85%** 以上。
