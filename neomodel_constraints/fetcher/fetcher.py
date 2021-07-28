from typing import List

from neomodel_constraints.connection import ConnectionAbstract
from neomodel_constraints.constraint import ConstraintSet, TypeMapperAbstract

from .abstract import ConstraintsFetcherAbstract
from .data import Neo4jConstraintQueryRecord


class ConstraintsFetcher(ConstraintsFetcherAbstract):
    def __init__(self, connection: ConnectionAbstract, type_mapper: TypeMapperAbstract):
        self.connection: ConnectionAbstract = connection
        self.type_mapper: TypeMapperAbstract = type_mapper

    def _fetch_raw_data(self) -> List[Neo4jConstraintQueryRecord]:  # TODO
        pass

    def _convert_constraints(self, raw: List[Neo4jConstraintQueryRecord]) -> ConstraintSet:  # TODO
        pass
