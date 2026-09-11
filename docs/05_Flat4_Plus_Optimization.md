# Flat-4+ 架构演进方案 (Flat-4+ Architecture Proposal)

基于原始的 Pardpro's Flat-4 架构，本方案旨在解决原架构在业务复用、纯领域建模以及简单查询流上的痛点。我们将这个优化版本称为 **Flat-4+ (增强版)**。

以下是完整的四个维度的优化与落地指导：

---

## 1. 引入 L0 领域层 (Domain/Core Layer)
**解决痛点**：消除 L2 过于臃肿的“贫血模型”，将“核心计算”与“业务编排”解耦。

### 核心规则：
- **无外部依赖**：L0 绝对不能包含任何与数据库、网络、框架相关的 I/O 操作。
- **纯粹的数据与规则**：存放充血模型 (Entities)、值对象 (Value Objects)、纯业务算法（如价格计算、规则校验）、状态机流转规则等。
- **调用流向**：L0 **不调用任何层**，它是被调用的底层。L2 负责从 L4 获取数据（如 DB 实体），将其转换为 L0 对象，并调用 L0 的纯函数完成核心业务计算。

### 示例代码流：
```python
# L0 (Domain)
class Order:
    def calculate_discount(self):
        # 纯内存计算，不查库
        pass 

# L2 (Coordinator)
def place_order_coordinator(context):
    raw_data = l4_fetch_order(context.order_id)
    order = Order(raw_data) # 组装 L0 对象
    discount = order.calculate_discount() # 纯业务计算
    l4_save_order(order)
```

---

## 2. 引入读写分离快速通道 (CQRS Fast-Track)
**解决痛点**：避免简单的查询操作（如获取列表、详情）也要走 `L1 -> L2 -> L4` 的繁琐样板代码。

### 核心规则：
- **写操作 (Command)**：涉及状态变更的操作，必须严格遵守 `L1 -> L2 -> L3/L4`。
- **读操作 (Query)**：对于纯数据读取（且无需复杂跨域编排），允许 **L1 直接调用 L4**（`L1 -> L4`）。
- **禁止副产物**：走快速通道的查询绝对不能修改数据，甚至不能记录带有业务含义的审计日志（如果需要记日志，说明是业务流，请退回 L2）。

### 依赖矩阵更新：
| Caller | May call | Must not call |
| --- | --- | --- |
| L1 | L2, **L4 (仅限查询)** | L1, L3 |

---

## 3. 标准化 L2 共享业务块 (Policies / Strategies)
**解决痛点**：因为禁止 `L2 -> L2`，当不同编排流有 80% 的共性时，无法复用业务逻辑。

### 核心规则：
- **Policy/Strategy 化**：提取共用的业务“策略片段”（如风控阻断、VIP权限校验），但不将它们变成另一个独立的 L2 编排器。
- **依赖注入**：将这些 Policy 视作一级公民，由 L1 实例化后，作为 **Context 的一部分**或**中间件**注入给 L2。
- **L3 不越权**：坚守原有规则，L3 依旧只负责“无状态的分子操作（例如: 发完邮件发短信的固定序列）”，不接管产品级业务分支。

### 落地方式：
```python
# Policy (共享业务块)
def fraud_check_policy(context):
    if context.user_score < 50:
        raise FraudException()

# L2 (Coordinator)
def checkout_l2(context, policies):
    for policy in policies:
        policy(context)  # 复用逻辑在这里执行
    
    # 专属的主编排流程...
```

---

## 4. 开放 Common/Utils 泛型层
**解决痛点**：严禁同层调用导致 L4 无法调用 L4，连用一个通用的字符串处理函数都违规。

### 核心规则：
- **跨层通用层**：建立一个完全独立的 `Utils/Common` 空间。
- **职责限制**：只存放与业务完全无关的技术型纯函数（如日期格式转换、加密解密算法、字符串清洗）。
- **全局可访问**：L1, L2, L3, L4 都可以不受限地调用 Utils，Utils 之间也可以互相调用。但 Utils 绝对不能反向调用 L0 到 L4 任何一层。

---

## 总结：Flat-4+ 优化后的依赖矩阵

| Caller | 职责定位 | 可调用 (May call) | 严禁调用 (Must not call) |
| --- | --- | --- | --- |
| **L1** | 路由、环境初始化、接收请求 | L2 (写/复杂读), L4(简单纯查), Utils | L1, L3, L0 |
| **L2** | 业务主编排、上下文管理、状态流转 | L3, L4, L0, Utils, Policies | L1, L2 |
| **L3** | 分子序列（聚合 L4 无状态操作） | L4, Utils | L1, L2, L3, L0 |
| **L4** | 原子操作（I/O、网络、单步外部调用） | Utils | L1, L2, L3, L4, L0 |
| **L0** | 纯领域模型、业务规则计算 (纯内存) | Utils | L1, L2, L3, L4, L0 |
| **Utils**| 纯技术型工具 | 同层其他 Utils | L0, L1, L2, L3, L4 |

*注：Policies 作为业务逻辑块，属于 L2 范畴的横向扩展，不打破 L2 的独立编排原则。*
