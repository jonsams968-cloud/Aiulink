from app.models import RiskLevel


def require_human_approval(risk: RiskLevel) -> bool:
    return risk in {RiskLevel.R3, RiskLevel.R4}
