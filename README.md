# Aiulink

人在回路（Human-in-the-Loop）的企业级自主代理网络工程骨架。

## 产品定位
Aiulink 本身就是企业系统：
- 先沉淀企业数据（本地导入/云导入）
- 再让主干 AI 基于私域数据进行决策、调度与汇报
- 员工通过自然语言创建“自代理（Personal Agent）”，而非写代码或连线

## 目标
- 让员工通过自然语言创建“自代理（Personal Agent）”，而不是写代码或画流程图。
- 由主干 AI 统一做权限调度、任务分发、汇总与报告。
- 默认自动化低风险任务，高风险任务触发人工确认。
- 通过一个高权限悬浮控制框实现全网可视化、接管与审计。
- 将“数据导入”作为 AI 决策前置条件。
- 为每个任务自动生成“任务责任单（Task Responsibility Card）”。

## Monorepo 结构

```text
.
├── backend/                 # FastAPI 控制面原型
│   ├── app/
│   │   ├── main.py          # API 入口
│   │   ├── models.py        # 核心数据模型
│   │   └── services/
│   │       ├── skill_builder.py
│   │       ├── orchestrator.py
│   │       ├── risk_engine.py
│   │       ├── data_import.py
│   │       └── responsibility.py
│   ├── tests/
│   │   ├── test_skill_builder.py
│   │   ├── test_data_import.py
│   │   └── test_responsibility.py
│   └── pyproject.toml
├── docs/
│   ├── architecture.md      # 工程框架设计
│   └── tech-route.md        # 技术路线（分阶段）
└── frontend/                # 预留：悬浮控制框与全网可视化
```

## 快速启动（后端原型）

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload --port 8080
```

打开 `http://127.0.0.1:8080/docs` 查看 OpenAPI。

## 当前能力（原型）
- `POST /v1/agents/from-natural-language`
  - 输入自然语言描述（例如“将 A 表格核对后同步到 B 表格”）。
  - 输出结构化代理定义（能力、数据域、风险等级、审批策略）。
- `POST /v1/tasks/plan`
  - 输入任务与上下文。
  - 输出由主干 AI 生成的执行计划（候选执行者、风险标记、是否需人工确认）。
- `POST /v1/data/import`
  - 输入本地或云数据来源信息。
  - 输出导入摘要（来源、数据集、风险等级、是否需人工确认）。
- `POST /v1/tasks/responsibility-card`
  - 输入任务发起者、审批者、数据集版本、代理调用与输出对象。
  - 输出责任归属、审批状态、决策轨迹和证据引用。

## 下一步建议
- 前端实现“悬浮控制框 + 任务时间线 + 责任归因”。
- 实现“数据导入中心”：版本化、字段映射、去重与血缘。
- 将 `risk_engine` 替换为可配置策略中心（策略即代码）。
