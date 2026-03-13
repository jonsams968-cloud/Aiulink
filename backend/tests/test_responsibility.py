from app.models import ResponsibilityCardRequest, RiskLevel
from app.services.responsibility import build_responsibility_card


def test_responsibility_card_requires_approval_for_high_risk() -> None:
    req = ResponsibilityCardRequest(
        task_id="task-001",
        initiator="user-a",
        approver="manager-b",
        datasets=["change_requests"],
        dataset_versions=["2026-03-13-v1"],
        agents_used=["ocr-agent", "dispatch-agent"],
        risk_level=RiskLevel.R3,
        output_targets=["internal://project-owner"],
        escalation_notes=["cross-domain-write"],
    )

    card = build_responsibility_card(req)

    assert card.approval_required is True
    assert card.accountability_owner == "manager-b"
    assert "approval=required:manager-b" in card.decision_trace
    assert card.evidence_refs == ["dataset://change_requests@2026-03-13-v1"]
