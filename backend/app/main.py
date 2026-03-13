from fastapi import FastAPI

from app.models import (
    AgentCreateRequest,
    AgentDefinition,
    DataImportRequest,
    DataImportResponse,
    TaskPlanRequest,
    TaskPlanResponse,
)
from app.services.data_import import import_dataset
from app.services.orchestrator import build_task_plan
from app.services.skill_builder import build_agent_from_natural_language

app = FastAPI(title="Aiulink Control Plane", version="0.2.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/agents/from-natural-language", response_model=AgentDefinition)
def create_agent(req: AgentCreateRequest) -> AgentDefinition:
    return build_agent_from_natural_language(req)


@app.post("/v1/tasks/plan", response_model=TaskPlanResponse)
def plan_task(req: TaskPlanRequest) -> TaskPlanResponse:
    return build_task_plan(req)


@app.post("/v1/data/import", response_model=DataImportResponse)
def import_data(req: DataImportRequest) -> DataImportResponse:
    return import_dataset(req)
