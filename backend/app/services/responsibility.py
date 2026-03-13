from app.models import ResponsibilityCardRequest, ResponsibilityCardResponse, RiskLevel
from app.services.risk_engine import require_human_approval


def build_responsibility_card(req: ResponsibilityCardRequest) -> ResponsibilityCardResponse:
    approval_required = require_human_approval(req.risk_level)

    owner = req.approver if approval_required and req.approver else req.initiator

    decision_trace = [
        f"initiator={req.initiator}",
        f"risk_level={req.risk_level.value}",
        f"agents={','.join(req.agents_used) if req.agents_used else 'none'}",
        f"datasets={','.join(req.datasets) if req.datasets else 'none'}",
    ]

    if approval_required:
        decision_trace.append(f"approval=required:{req.approver or 'pending'}")
    else:
        decision_trace.append("approval=not_required")

    if req.escalation_notes:
        decision_trace.append(f"escalations={';'.join(req.escalation_notes)}")

    evidence_refs = []
    for name, version in zip(req.datasets, req.dataset_versions):
        evidence_refs.append(f"dataset://{name}@{version}")

    if not evidence_refs and req.datasets:
        evidence_refs = [f"dataset://{name}@latest" for name in req.datasets]

    return ResponsibilityCardResponse(
        task_id=req.task_id,
        accountability_owner=owner,
        approval_required=approval_required,
        decision_trace=decision_trace,
        evidence_refs=evidence_refs,
        output_targets=req.output_targets,
        status="approved" if approval_required and req.approver else "in_progress",
    )
