# ADR-003: 零垃圾回收内存契约 (Zero-GC Memory Arena Contract)

**Date**: 2026-XX-XX  
**Status**: Accepted  
**Context**: Project A & B / Flat-4 Architecture Core  

## 背景与技术不确定性 (Technological Uncertainty)
在嵌入式设备及高频控制系统（>100Hz）中，传统的面向对象编程范式会导致极高的内存分配与销毁开销。在 Python, C#, JS 等带有垃圾回收 (GC) 机制的语言中，频繁的堆内存分配会导致难以预测的 GC 停顿 (GC Pauses/Spikes)，从而打破严格的 <16ms 延迟预算。
技术不确定性在于：如何在保证 Flat-4 严格的分层和解耦的同时，彻底消除高频业务主循环中的内存抖动？

## 实验与迭代过程 (Systematic Investigation)
1. **默认运行时分配**：早期我们在 L2 的循环中，每次响应传感器事件都实例化新的上下文对象（Context Object）并传递给 L3/L4。当事件流达到 100Hz 时，GC 会每隔几秒触发一次 Stop-The-World 停顿，导致严重的帧延迟或硬件信号漏捕。
2. **零分配 (Zero-Allocation) 原则验证**：我们参考了游戏引擎与高频交易框架的思路，在架构级引入了 **Memory Arena (对象池/内存竞技场)** 的概念。并验证了如果取消所有高频代码路径中的 `new` 或动态分配，系统的延迟抖动（Jitter）将趋近于零。

## 决策 (Decision)
在 Flat-4+ 规范中，正式确立针对高性能场景的 **“零 GC (Zero-GC)” 强制契约**：

1. **预分配责任 (L1)**：所有的内存缓冲、对象池、事件上下文容器（Context Arena），必须在系统启动时由 L1 (Entry Layer) 一次性预分配完毕。
2. **原地修改 (L2)**：L2 (Coordinator) 在核心事件循环中，**严禁使用任何动态内存分配（如 `new`, `malloc`，或创建临时对象）**。L2 只能向 L1 预分配好的 Arena 借用内存，并通过原地修改 (In-place mutation) 更新状态。
3. **零拷贝穿透 (L3/L4)**：穿透 L2 传向 L3/L4 的数据，必须是底层缓冲区的直接引用或指针（Zero-Copy Pipeline），保证数据的读取与下发不产生任何中间拷贝开销。

## 影响与技术进步 (Advancement)
- **技术突破**：在应用此架构契约后，业务代码在高频运行下的 GC 停顿问题被彻底根除。系统端到端延迟变得极其平滑且可预测，为后续的热反压控制和微秒级调度奠定了稳定的时间轴基础。
- **架构影响**：Flat-4 架构具备了从企业级应用平滑降维至嵌入式/硬实时 (Hard Real-Time) 环境的能力，确立了其极高的系统级编程门槛。
