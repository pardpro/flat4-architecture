# ADR-001: 强制 L4 隔离以规避 OS 电源管理与 Watchdog

**Date**: 2026-XX-XX  
**Status**: Accepted  
**Context**: Project A / Flat-4 Architecture Core  

## 背景与技术不确定性 (Technological Uncertainty)
在嵌入式设备及现代桌面操作系统（如 Windows Modern Standby, macOS App Nap）中，操作系统会为了省电而积极地限制或挂起后台的 USB/HID 通信。
我们需要实现**微秒级 (Microsecond-level) 的硬件轮询**以保证数据的实时性（延迟 < 16ms），但面临着极大的技术不确定性：如何在纯用户态 (User-space) 完成极高频的轮询，同时不触发 OS 级别的 Watchdog 导致进程被杀，且不至于让电池电量迅速耗尽？

## 实验与迭代过程 (Systematic Investigation)
我们在架构上进行了多次尝试与失败：

1. **Iteration 1 (依赖标准 OS 调度器)**：我们最初尝试在 L2 或传统 Service 层使用系统原生的后台 Worker 机制。结果：OS 会动态将后台唤醒间隔延迟至几分钟，导致“近实时更新”完全失败。
2. **Iteration 2 (低优先级常驻轮询线程)**：我们在 L4 引入了一个伴有指数退避 (Exponential Backoff) 算法的持久后台线程。结果：虽然数据保持了最新，但持续的 CPU 唤醒迅速耗尽了电池；更为严重的是，OS Watchdog 将这种持续唤醒归类为“异常后台占用”，直接将其强杀。
3. **Iteration 3 (L4 防抖微突发机制 + 增量事件驱动)**：我们决定全面利用 Flat-4 的隔离特性。L4 被设计为绝对隔离，我们构建了一个“基于增量状态的事件驱动同步 (Delta-State Event-Driven Sync)”机制。系统在物理状态跨越阈值前保持完全休眠。一旦触发，L4 执行一个带有防抖的“微突发滑动窗口 (<5ms 执行切片)”，然后迅速交还控制权给 L2。

## 决策 (Decision)
**强制规定：所有涉及抗睡眠、硬件轮询以及底层微调的逻辑，必须被严格死锁在 L4 层。** 
L2 (Coordinator) 绝对不允许直接调用 OS 线程接口或轮询硬件。L2 只能响应 L4 通过增量事件抛出的明确信号。

## 影响与技术进步 (Advancement)
- **技术突破**：通过 L4 执行 5ms 内的微突发切片，完美骗过了 OS Watchdog，将闲置功耗降至最低，同时保障了活动期间 <16ms 的端到端延迟。
- **架构影响**：巩固了 Flat-4 中 L4 层作为“唯一副作用与硬件边界”的原则，使得该解决方案可以安全地复用到后续所有跨平台项目中。
