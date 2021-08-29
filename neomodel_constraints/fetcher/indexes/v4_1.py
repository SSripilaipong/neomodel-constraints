from typing import List, Dict

from neomodel_constraints.connection import ConnectionAbstract
from neomodel_constraints.constraint import ConstraintSet, TypeMapperAbstract
from neomodel_constraints.fetcher.abstract import FetcherAbstract

from .data import Neo4jIndexQueryRecord


def convert_record(record: Dict) -> Dict:
    record['indexProvider'] = record['provider']
    del record['provider']
    return record


class IndexesOnlyFetcher(FetcherAbstract):
    def __init__(self, connection: ConnectionAbstract, type_mapper: TypeMapperAbstract):
        self.connection: ConnectionAbstract = connection
        self.type_mapper: TypeMapperAbstract = type_mapper

    def _fetch_raw_data(self) -> List[Neo4jIndexQueryRecord]:
        raw = self.connection.execute('CALL db.indexes')
        converted_records = [convert_record(r) for r in raw]
        records = [Neo4jIndexQueryRecord(**record) for record in converted_records]
        return [r for r in records
                if r.uniqueness == 'NONUNIQUE'
                and r.type_ != 'LOOKUP'
                and r.entity_type == 'NODE']

    def _convert_index(self, raw: List[Neo4jIndexQueryRecord]) -> ConstraintSet:
        constraints = set()
        for record in raw:
            constraint_type = self.type_mapper.map('NONUNIQUE_INDEX')
            constraint = constraint_type.from_raw(record.dict())
            constraints.add(constraint)
        return ConstraintSet(constraints)

    def fetch(self) -> ConstraintSet:
        raw: List[Neo4jIndexQueryRecord] = self._fetch_raw_data()
        constraints: ConstraintSet[IndexesOnlyFetcher] = self._convert_index(raw)
        return constraints
