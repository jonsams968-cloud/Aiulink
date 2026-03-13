# 工程框架设计

## 1. 设计原则

1. **Aiulink 本身即企业系统**：不依赖第三方办公系统也可独立运行。
2. **身份先于连接**：人、设备、代理入网必须完成身份核验。
3. **数据先于决策**：AI 决策必须有企业私域数据支撑。
4. **能力最小化授权**：代理只拿到执行任务所需最小能力。
5. **低风险自动，高风险人工**：风险分层驱动自动化边界。
6. **全链路可追溯**：每次决策、调用、分发都可审计。

## 2. 核心模块

### A. Identity & Trust（身份与信任）
- 对象：`HumanNode`、`DeviceNode`、`AgentNode`
- 能力：SSO/OIDC、设备指纹、代理签名、会话有效期

### B. Data Import Hub（数据导入中心）
- 导入来源：
  - 本地文件（CSV/Excel/PDF/图片）
  - 云存储对象（bucket/path）
- 处理流程：
  - 文件解析 / OCR / 字段映射 / 去重 / 版本化
- 输出结果：
  - `Dataset`（结构化数据）
  - `Evidence`（原始证据与快照）

### C. Enterprise Knowledge Layer（企业知识层）
- 数据目录（数据集、字段、Owner、更新时间）
- 向量与关键词混合检索
- 权限切片（组织/项目/字段级）

### D. Capability Registry（能力注册中心）
- 每个节点可发布自己的代理能力（例如 OCR、表格校验、项目分发）。
- 发布时附带：
  - 适用范围（部门/项目）
  - 风险等级上限
  - 数据权限范围
  - SLA/成本

### E. Backbone Orchestrator（主干 AI）
- 任务理解与拆解
- 基于数据目录选择可用数据源
- 代理候选选择与权限校验
- 分发执行与汇总报告
- 冲突仲裁（多代理结果冲突时）

### F. Human-in-the-Loop Gateway（人在回路网关）
触发条件：
- 跨域数据写入
- 风险等级 ≥ R3
- 低置信度或冲突结论
- 责任主体不清晰

### G. Task Responsibility Card（任务责任单）
- 每个任务自动固化：
  - 发起人、审批人、责任人
  - 数据集与版本号
  - 调用代理与动作轨迹
  - 输出对象与分发范围
  - 升级/接管记录
- 用于审计、回放、责任归因与复盘

### H. Floating Control Box（高权限悬浮框）
- 一键查看：当前任务、执行链路、责任主体、风险状态
- 一键操作：批准 / 驳回 / 接管 / 重新分发
- 一键追溯：查看证据、输入来源、操作日志

## 3. 数据流（示例）

1. 用户输入：
   “把甲方图片里的修改意见 OCR 后，按项目匹配负责人并分发。”
2. 数据导入中心先处理：
   - 图片 OCR -> 结构化修改项
   - 负责人映射表导入 -> 可查询数据集
3. 主干 AI 生成计划：
   - OCR 代理
   - 项目匹配代理
   - 负责人映射代理
   - 通知分发代理
4. 风险网关判断：
   - 若仅内部通知 -> R1/R2 自动执行
   - 若外发甲方/关键系统写入 -> R3 人工确认
5. 同步生成任务责任单：
   - 固化数据版本、审批记录、责任主体与证据引用
6. 最终汇总：
   - 完成项
   - 未匹配项
   - 人工介入记录

## 4. 推荐部署拓扑

- `control-plane`：调度、策略、审计 API（FastAPI）
- `data-ingestion`：导入、OCR、ETL 管线
- `knowledge-store`：Postgres + Vector Index + Object Storage
- `agent-runtime`：代理执行容器池（Kubernetes Jobs / Celery workers）
- `event-bus`：NATS / Kafka（任务与状态事件）
- `policy-store`：OPA
- `observability`：OpenTelemetry + Prometheus + Loki + Tempo
