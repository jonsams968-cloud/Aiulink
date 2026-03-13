from app.models import RiskLevel, TaskPlanRequest, TaskPlanResponse, TaskStep
from app.services.risk_engine import require_human_approval


def build_task_plan(req: TaskPlanRequest) -> TaskPlanResponse:
    task = req.task
    lower = task.lower()

    steps = []

    if "图片" in lower or "ocr" in lower:
        risk = RiskLevel.R2
        steps.append(
            TaskStep(
                step="OCR 提取修改意见",
                selected_agent="ocr-agent",
                risk_level=risk,
                require_human_approval=require_human_approval(risk),
            )
        )

    if "表格" in lower or "a" in lower and "b" in lower:
        risk = RiskLevel.R2
        steps.append(
            TaskStep(
                step="A/B 表格比对与状态核对",
                selected_agent="sheet-agent",
                risk_level=risk,
                require_human_approval=require_human_approval(risk),
            )
        )

    if "甲方" in lower or "外发" in lower or "发送" in lower:
        risk = RiskLevel.R3
        steps.append(
            TaskStep(
                step="按负责人分发修改建议",
                selected_agent="dispatch-agent",
                risk_level=risk,
                require_human_approval=require_human_approval(risk),
            )
        )

    if not steps:
        risk = RiskLevel.R1
        steps.append(
            TaskStep(
                step="通用任务处理",
                selected_agent="general-agent",
                risk_level=risk,
                require_human_approval=require_human_approval(risk),
            )
        )

    return TaskPlanResponse(summary="主干 AI 已生成执行计划", steps=steps)
