from app.models import AgentCreateRequest, AgentDefinition, Capability, RiskLevel


def build_agent_from_natural_language(req: AgentCreateRequest) -> AgentDefinition:
    """
    轻量原型：将自然语言需求映射为结构化代理定义。
    真实版本建议替换为 LLM + policy guardrails。
    """
    text = req.natural_language_spec.lower()

    capabilities = []
    domain = "general"
    risk_ceiling = RiskLevel.R2

    if "ocr" in text or "图片" in text:
        capabilities.append(Capability(name="ocr_extract", description="从图片提取文字"))
        domain = "document-processing"

    if "表格" in text or "excel" in text:
        capabilities.append(Capability(name="sheet_reconcile", description="表格比对与校验"))
        domain = "spreadsheet-ops"

    if "分发" in text or "通知" in text:
        capabilities.append(Capability(name="dispatch_message", description="将结果分发给负责人"))

    if "外部" in text or "甲方" in text:
        risk_ceiling = RiskLevel.R3

    if not capabilities:
        capabilities.append(Capability(name="task_assistant", description="通用任务辅助"))

    return AgentDefinition(
        name=f"agent-{req.owner_node_id}",
        owner_node_id=req.owner_node_id,
        domain=domain,
        capabilities=capabilities,
        risk_ceiling=risk_ceiling,
        shared_to_network=True,
    )
