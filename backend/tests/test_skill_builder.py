from app.models import AgentCreateRequest, RiskLevel
from app.services.skill_builder import build_agent_from_natural_language


def test_build_agent_for_ocr_and_sheet_flow() -> None:
    req = AgentCreateRequest(
        owner_node_id="u-001",
        natural_language_spec="将甲方图片建议ocr后和表格核对，并分发给负责人",
    )
    result = build_agent_from_natural_language(req)

    names = {cap.name for cap in result.capabilities}
    assert "ocr_extract" in names
    assert "sheet_reconcile" in names
    assert "dispatch_message" in names
    assert result.risk_ceiling == RiskLevel.R3
