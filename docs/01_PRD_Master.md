# F4A Product Brief & Specification Template

**Project / Subsystem:** [名称]
**Primary Profile:** [SaaS | Hardware / Realtime | AI Agent | Content / Data]
**Risk:** [Low / Standard / High / Critical]
**Status:** [Draft / Approved]
**Owner:** [负责人]

## 1. Frame

- **User / Operator:** 谁遇到问题？
- **Problem:** 当前痛点和证据是什么？
- **Outcome:** 用户可观察到的成功结果是什么？
- **Non-goals:** 本次明确不做什么？

## 2. Boundaries

- **Deployment boundary:** 该子系统如何独立部署和运行？
- **Trust boundary:** 哪些输入、用户或服务不可信？
- **Data boundary:** 处理什么数据，谁拥有，保存多久？
- **External systems:** 数据库、支付、AI、设备、第三方服务有哪些？

## 3. Behavior

描述主路径，并补充适用的空状态、失败、权限、并发、超时、重试、恢复和回滚行为。

## 4. Acceptance

使用可验证条件，不使用“正常”“快速”“智能”等无法测量的描述。

- [ ] [成功条件]
- [ ] [失败/空状态条件]
- [ ] [权限/安全条件]
- [ ] [恢复/回滚条件]
- [ ] [产品特定指标与测量方法]

## 5. Evidence plan

列出与风险等级相称的测试、评审、遥测、迁移、硬件台架或人工验收证据。
