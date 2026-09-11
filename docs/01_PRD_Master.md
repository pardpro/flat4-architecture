# Product Requirement Document (PRD)

**Project:** [项目名称]
**Version:** 2.0 (Flat-4+)
**Status:** Draft / Approved
**Date:** 2026-XX-XX

## 1. Objective (目标)
> 用一句话清晰描述：L2 协调层或 L1 快速通道最终要完成什么任务？
> 例：完成从用户发起核心指令到最终底层硬件输出响应的全过程调度。

## 2. Business Logic & Flows (业务逻辑流)
> **这是 L2 Coordinator 和 L0 Domain 的设计蓝本，请详细列出步骤。**

### 核心写操作流程 A：[例如：数据流计算与下发]
1. 用户发起请求（L1 接收输入：参数X）。
2. L1 调用 L2，L2 预分配并初始化上下文 (Context Arena，符合零 GC 契约)。
3. L2 调用 L4 原子能力采集底层数据。
4. L2 调用 L0 (纯数据算法) 进行数据计算或逻辑预测。
5. L2 基于 L0 的结果，通过 L3 组合管道下发给 L4 硬件驱动。
6. 如果底层硬件通过 L4 抛出“温度超标”或“防抖微突发失败”的反压信号，L2 执行重试或回滚。

### 核心读操作流程 B：[例如：查询设备状态 (CQRS 快速通道)]
1. L1 接收查询请求。
2. L1 绕过 L2，直接调用 L4 原子读取数据库或硬件状态。
3. L1 返回给用户。

## 3. Data Context (上下文数据)
> L2 层需要全程持有的数据有哪些？
* **Context Arena:** [必须符合 Zero-GC 预分配契约]
* **Input Data:** [e.g., UserID, RequestType]
* **State Data:** [e.g., RetryCount, ThermalState]

> L0 提供纯数据模型，L2 统一管理状态。L3/L4 仅接受零拷贝引用 (Zero-Copy References)。

## 4. Hardware & Performance Constraints (硬件与性能约束)
* **Latency:** [e.g., 端到端延迟 < 16ms]
* **OS Power Management:** [必须通过 L4 隔离 OS 休眠与 Watchdog]
* **Memory:** [高频循环内 0 动态分配, 0 GC Spikes]
* **Safety:** [e.g., 核心温度 > 48°C 时，L2 必须介入主动丢帧]
