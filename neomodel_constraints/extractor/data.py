from typing import Set
from enum import Enum

from pydantic import BaseModel


class ConstraintType(str, Enum):
    UNIQUE_INDEX = 'UNIQUE_INDEX'


class ExtractedConstraintRecord(BaseModel):
    type_: ConstraintType
    labels: Set[str]
    name: str
