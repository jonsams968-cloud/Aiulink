from dataclasses import dataclass, field
from enum import Enum


class RiskLevel(str, Enum):
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"
    R4 = "R4"


class DataSourceType(str, Enum):
    LOCAL = "local"
    CLOUD = "cloud"


@dataclass
class Capability:
    name: str
    description: str


@dataclass
class AgentDefinition:
    name: str
    owner_node_id: str
    domain: str
    capabilities: list[Capability]
    risk_ceiling: RiskLevel = RiskLevel.R2
    shared_to_network: bool = False


@dataclass
class AgentCreateRequest:
    owner_node_id: str
    natural_language_spec: str


@dataclass
class TaskPlanRequest:
    task: str
    candidate_agents: list[AgentDefinition] = field(default_factory=list)


@dataclass
class TaskStep:
    step: str
    selected_agent: str
    risk_level: RiskLevel
    require_human_approval: bool


@dataclass
class TaskPlanResponse:
    summary: str
    steps: list[TaskStep]


@dataclass
class DataImportRequest:
    source_type: DataSourceType
    source_uri: str
    dataset_name: str


@dataclass
class DataImportResponse:
    dataset_name: str
    source_type: DataSourceType
    records_estimated: int
    risk_level: RiskLevel
    require_human_approval: bool
    note: str
