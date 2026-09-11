**（对应角色：Inspector）**
> **核心用途：** 针对 Flat-4+ 的分层测试策略。

# Test Strategy & Plan (Flat-4+)

## 1. L0 & Utils Unit Tests (纯逻辑测试)
> **策略：** 因为 L0 和 Utils 没有任何依赖与副作用，测试必须做到 100% 覆盖率。
> **要求：** 输入任意边界值，验证纯函数的数学或字符串计算的确定性。

## 2. L4 Unit Tests (原子测试)
> **策略：** 针对外部副作用进行沙盒隔离测试。
- [ ] **Context Isolation:** L4 测试不依赖复杂的 L2 Context，所需数据均由显式参数传入。
- [ ] **Hardware Mock:** 针对防抖和轮询，注入模拟时钟 (Mock Clock) 验证其是否触发微突发限制。
- [ ] **Watchdog Tolerance:** 验证错误代码是否正确冒泡而不导致主进程崩溃。

## 3. L2 Integration Tests (调度测试)
> **策略：** 注入 L4 和 L0 的替身，只测试 L2 的**状态机流转与热反压管理**。
- [ ] **Zero-GC Compliance:** 开启内存 Profiler，确认在 10,000 次模拟事件循环内，内存分配 (Allocations) 计数为 0。
- [ ] **Error/Thermal Handling:** 当底层替身抛出高温信号或超时，L2 是否按策略执行了主动丢帧或回滚。

## 4. Manual / AI Acceptance Tests (验收标准)
- [ ] AI 在现有架构下新加 L4 特性时，Pass@1 是否大于 85% (参照 `06_Evaluation_Metrics.md`)。
- [ ] WPA/Instruments 实机压测下，CPU 唤醒降低幅度是否达标。
