from typing import List
from enum import Enum

from pydantic import BaseModel


class ConstraintType(str, Enum):
    UNIQUE_INDEX = 'UNIQUE_INDEX'


class ExtractedConstraintRecord(BaseModel):
    type_: ConstraintType
    labels: List[str]
    name: str
