from typing import List
from enum import Enum
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    NODE: str = "NODE"
    RELATIONSHIP: str = "RELATIONSHIP"


class IndexType(str, Enum):
    BTREE: str = "BTREE"
    FULLTEXT: str = "FULLTEXT"


class Uniqueness(str, Enum):
    UNIQUE: str = "UNIQUE"
    NONUNIQUE: str = "NONUNIQUE"


class Neo4jIndexQueryRecord(BaseModel):
    id_: int = Field(..., alias="id")
    population_percent: float = Field(..., alias="populationPercent")
    type_: IndexType = Field(..., alias="type")
    entity_type: EntityType = Field(..., alias="entityType")
    labels_or_types: List[str] = Field(..., alias="labelsOrTypes")
    index_provider: str = Field(..., alias="indexProvider")
    name: str
    properties: List[str]
    state: str
    uniqueness: Uniqueness
