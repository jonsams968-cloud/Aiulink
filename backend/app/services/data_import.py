from app.models import DataImportRequest, DataImportResponse, RiskLevel
from app.services.risk_engine import require_human_approval


def import_dataset(req: DataImportRequest) -> DataImportResponse:
    """
    原型版本：根据来源类型和路径特征做轻量风险判断。
    后续可替换为真实 ETL/OCR/Schema Mapping 管线。
    """
    uri = req.source_uri.lower()
    risk = RiskLevel.R1

    if req.source_type.value == "cloud":
        risk = RiskLevel.R2

    if any(token in uri for token in ["external", "vendor", "甲方", "public"]):
        risk = RiskLevel.R3

    estimated = 100
    if "large" in uri or "gb" in uri:
        estimated = 100000

    return DataImportResponse(
        dataset_name=req.dataset_name,
        source_type=req.source_type,
        records_estimated=estimated,
        risk_level=risk,
        require_human_approval=require_human_approval(risk),
        note="数据已进入导入队列，等待解析与索引。",
    )
