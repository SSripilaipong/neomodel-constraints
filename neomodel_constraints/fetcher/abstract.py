from typing import List, Dict
from abc import ABC, abstractmethod

from neomodel_constraints.constraint.set import ConstraintSet

from .data import Neo4jConstraintQueryRecord


class ConstraintsFetcherAbstract(ABC):
    @abstractmethod
    def _fetch_raw_data(self) -> List[Neo4jConstraintQueryRecord]:
        pass

    @abstractmethod
    def _convert_constraints(self, raw: List[Neo4jConstraintQueryRecord]) -> ConstraintSet:
        pass

    def fetch(self) -> ConstraintSet:
        raw: List[Neo4jConstraintQueryRecord] = self._fetch_raw_data()
        constraints: ConstraintSet = self._convert_constraints(raw)
        return constraints
