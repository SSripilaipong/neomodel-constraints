from typing import List

from neomodel_constraints.connection import ConnectionAbstract
from neomodel_constraints.constraint import ConstraintSet, TypeMapperAbstract

from neomodel_constraints.fetcher.abstract import FetcherAbstract
from neomodel_constraints.fetcher.constraints.data import Neo4jConstraintQueryRecord


class ConstraintsFetcherV4s2(FetcherAbstract):
    def __init__(self, connection: ConnectionAbstract, type_mapper: TypeMapperAbstract):
        self.connection: ConnectionAbstract = connection
        self.type_mapper: TypeMapperAbstract = type_mapper

    def _fetch_raw_data(self) -> List[Neo4jConstraintQueryRecord]:
        raw = self.connection.execute('SHOW CONSTRAINTS')
        return [Neo4jConstraintQueryRecord(**record) for record in raw]

    def _convert_constraints(self, raw: List[Neo4jConstraintQueryRecord]) -> ConstraintSet:
        constraints = set()
        for record in raw:
            constraint_type = self.type_mapper.map(record.type_)
            constraint = constraint_type.from_raw(record.dict())
            constraints.add(constraint)
        return ConstraintSet(constraints)

    def fetch(self) -> ConstraintSet:
        raw: List[Neo4jConstraintQueryRecord] = self._fetch_raw_data()
        constraints: ConstraintSet = self._convert_constraints(raw)
        return constraints
