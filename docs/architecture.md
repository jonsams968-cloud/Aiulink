# 工程框架设计

## 1. 设计原则

1. **身份先于连接**：人、设备、代理入网必须完成身份核验。
2. **能力最小化授权**：代理只拿到执行任务所需最小能力。
3. **低风险自动，高风险人工**：风险分层驱动自动化边界。
4. **全链路可追溯**：每次决策、调用、分发都可审计。

## 2. 核心模块

### A. Identity & Trust（身份与信任）
- 对象：`HumanNode`、`DeviceNode`、`AgentNode`
- 能力：SSO/OIDC、设备指纹、代理签名、会话有效期

### B. Capability Registry（能力注册中心）
- 每个节点可发布自己的代理能力（例如 OCR、表格校验、项目分发）。
- 发布时附带：
  - 适用范围（部门/项目）
  - 风险等级上限
  - 数据权限范围
  - SLA/成本

### C. Backbone Orchestrator（主干 AI）
- 任务理解与拆解
- 代理候选选择与权限校验
- 分发执行与汇总报告
- 冲突仲裁（多代理结果冲突时）

### D. Human-in-the-Loop Gateway（人在回路网关）
触发条件：
- 跨域数据写入
- 风险等级 ≥ R3
- 低置信度或冲突结论
- 责任主体不清晰

### E. Floating Control Box（高权限悬浮框）
- 一键查看：当前任务、执行链路、责任主体、风险状态
- 一键操作：批准 / 驳回 / 接管 / 重新分发
- 一键追溯：查看证据、输入来源、操作日志

## 3. 数据流（示例）

1. 用户输入：
   “把甲方图片里的修改意见 OCR 后，按项目匹配负责人并分发。”
2. 主干 AI 生成计划：
   - OCR 代理
   - 项目匹配代理
   - 负责人映射代理
   - IM/邮件分发代理
3. 风险网关判断：
   - 若仅内部通知 -> R1/R2 自动执行
   - 若外发甲方/关键系统写入 -> R3 人工确认
4. 最终汇总：
   - 完成项
   - 未匹配项
   - 人工介入记录

## 4. 推荐部署拓扑

- `control-plane`：调度、策略、审计 API（FastAPI）
- `agent-runtime`：代理执行容器池（Kubernetes Jobs / Celery workers）
- `event-bus`：NATS / Kafka（任务与状态事件）
- `policy-store`：Postgres + OPA
- `observability`：OpenTelemetry + Prometheus + Loki + Tempo
