from app.models import DataImportRequest, DataSourceType, RiskLevel
from app.services.data_import import import_dataset


def test_cloud_external_import_requires_human_approval() -> None:
    req = DataImportRequest(
        source_type=DataSourceType.CLOUD,
        source_uri="s3://vendor-external-bucket/project-change-large",
        dataset_name="project_change_requests",
    )
    result = import_dataset(req)

    assert result.risk_level == RiskLevel.R3
    assert result.require_human_approval is True
    assert result.records_estimated == 100000
