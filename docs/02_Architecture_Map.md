# Architecture Map (Flat-4+ Definition)

## 1. Structure Overview
遵循 Flat-4+ 增强架构。支持 CQRS 快速通道与 L0 纯算法层。

- **写操作 (Command/Complex):** `L1 (Entry) -> L2 (Coordinator) -> [L0 / L3 / L4 / Utils]`
- **读操作 (Query/Simple):** `L1 (Entry) -> L4 (Atomic)`

## 2. Layer Mapping (组件映射表)

### L0: Domain Layer (领域层)
> **职责：** 纯算法、数据结构，无任何 I/O 与副作用。
| Component Name | Type | Description |
| :--- | :--- | :--- |
| `CoreMath` | Algorithm | 核心预测算法，不依赖外部环境。 |

### L1: Entry Layer (入口层)
> **职责：** 接收请求，路由分发（写走 L2，读走 L4）。
| Component Name | Type | Description |
| :--- | :--- | :--- |
| `MainEntry.py` | API | 解析参数，读请求调 L4，写请求调 L2。 |

### L2: Coordinator Layer (指挥官)
> **职责：** 状态机与流程编排。管理 Zero-GC Context。
| Component Name | Context Held | Flows Managed |
| :--- | :--- | :--- |
| `SystemCoordinator` | UserReq, Arena | 负责主业务逻辑流转与热反压异常处理。 |

### L3: Molecular Layer (分子层 - 可选)
> **职责：** L4 的无状态序列封装，严禁 Mutex 锁。
| Component Name | Composed Atoms | Description |
| :--- | :--- | :--- |
| `DataPipeline_Mol` | `Fetch`, `Close` | 零拷贝的高频数据管线。 |

### L4: Atomic Layer (原子层)
> **职责：** 隔离外部副作用、微秒级防抖、对抗 OS 睡眠机制。
| Component Name | Input | Output | Description |
| :--- | :--- | :--- | :--- |
| `Sensor_Driver` | PortID | Reference | 防抖读取高频传感器原始数据。 |

### Utils: Common Layer (通用层)
> **职责：** 纯技术工具类，全层可用。

## 3. Dependency Check (依赖检查)
- [ ] L2 不调用 L2，L3 不调用 L3，L4 不调用 L4。
- [ ] 没有任何反向调用。
- [ ] L0 与 Utils 未被业务状态污染。
- [ ] 静态检查脚本已验证（AST Deep Scan）。
