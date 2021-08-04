from typing import List

from neomodel_constraints.connection import ConnectionAbstract
from neomodel_constraints.constraint import ConstraintSet, TypeMapperAbstract
from neomodel_constraints.fetcher.abstract import FetcherAbstract

from .data import Neo4jConstraintQueryRecord
from .util import convert_constraints_with_type_mapper


class ConstraintsFetcherV4s2(FetcherAbstract):
    def __init__(self, connection: ConnectionAbstract, type_mapper: TypeMapperAbstract):
        self.connection: ConnectionAbstract = connection
        self.type_mapper: TypeMapperAbstract = type_mapper

    def _fetch_raw_data(self) -> List[Neo4jConstraintQueryRecord]:
        raw = self.connection.execute('SHOW CONSTRAINTS')
        return [Neo4jConstraintQueryRecord(**record) for record in raw]

    def _convert_constraints(self, raw: List[Neo4jConstraintQueryRecord]) -> ConstraintSet:
        return convert_constraints_with_type_mapper(raw, self.type_mapper)

    def fetch(self) -> ConstraintSet:
        raw: List[Neo4jConstraintQueryRecord] = self._fetch_raw_data()
        constraints: ConstraintSet = self._convert_constraints(raw)
        return constraints
