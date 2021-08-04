from typing import List
from enum import Enum
from pydantic import BaseModel, Field


class ConstraintType(str, Enum):
    UNIQUENESS = 'UNIQUENESS'


class EntityType(str, Enum):
    NODE = 'NODE'
    RELATIONSHIP = 'RELATIONSHIP'


class Neo4jConstraintQueryRecord(BaseModel):
    id_: int = Field(..., alias='id')
    owned_index_id: int = Field(..., alias='ownedIndexId')
    entity_type: EntityType = Field(..., alias='entityType')
    labels_or_types: List[str] = Field(..., alias='labelsOrTypes')
    type_: ConstraintType = Field(..., alias='type')
    name: str
    properties: List[str]
