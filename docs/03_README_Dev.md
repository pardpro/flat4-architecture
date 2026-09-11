# Developer Guide & Rules (Flat-4+)

## ⚠️ CRITICAL: Development Standards
本项目严格遵循 **Flat-4+ Architecture** 与 **SR&ED 高性能硬件契约**。

### 1. The 6-Layer Rules
* **L0 (Domain):** 纯业务逻辑、算法与数据实体。不包含任何 I/O 或数据库连接。
* **L1 (Entry):** 路由与入口。写操作调 L2，只读查询可直调 L4 (CQRS)。
* **L2 (Coordinator):** 业务调度中心。持有预分配的 Context Arena，负责重试、回滚与高层控制逻辑。**禁止使用动态分配 (Zero-GC)**。
* **L3 (Molecular):** 无状态的 L4 序列组合。禁止跨线程锁，以保证 100Hz 无阻滞数据流。
* **L4 (Atomic):** 绝对独立的副作用单元。负责数据库、网络、模型推理及**微秒级硬件防抖**（隔离 OS Watchdog 唤醒机制）。
* **Utils (Common):** 全局纯技术通用函数（如时间戳转换）。

### 2. Directory Structure (目录结构)
请保持以下物理文件夹结构：
```text
/src
  /L0_Domain       # entities/, pure_math/
  /L1_Entry        # main.py, api_server.py
  /L2_Coordinator  # logic_controllers/
  /L3_Molecular    # (Optional) pipelines/
  /L4_Atomic       # utils/, tools/, drivers/
  /Utils           # string_utils/, date_utils/
```

### 3. Allowed Dependencies (依赖矩阵)
1. L2 统管全局 `L2 -> L0, L3, L4`
2. 同层严格隔离，不准互调 (除 Utils 外)。
3. 任何逆向调用直接在 CI/CD 中被 AST Scanner 拒绝。
