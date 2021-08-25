import re
from typing import List, Dict

from neomodel_constraints.connection import ConnectionAbstract
from neomodel_constraints.constraint import ConstraintSet, TypeMapperAbstract
from neomodel_constraints.fetcher.abstract import FetcherAbstract

from .data import Neo4jConstraintQueryRecord
from .util import convert_constraints_with_type_mapper


def extract_record_detail(detail: str) -> Dict:
    param_str = re.findall(r'^Constraint\((.*)\)$', detail)[0]
    id_ = re.findall(r"id=(\d+?),", param_str)[0]
    name = re.findall(r"name='(\w+?)',", param_str)[0]
    type_ = re.findall(r"type='(\w+?)',", param_str)[0]
    label, prop = re.findall(r"schema=\(:([^ ]+) {(\w+)}\)", param_str)[0]
    owned_index = re.findall(r"ownedIndex=(\d+)", param_str)[0]
    return {
        'id': id_,
        'ownedIndexId': owned_index,
        'entityType': 'NODE',
        'labelsOrTypes': [label],
        'type': type_,
        'name': name,
        'properties': [prop],
    }


class ConstraintsFetcher(FetcherAbstract):
    def __init__(self, connection: ConnectionAbstract, type_mapper: TypeMapperAbstract):
        self.connection: ConnectionAbstract = connection
        self.type_mapper: TypeMapperAbstract = type_mapper

    def _fetch_raw_data(self) -> List[Neo4jConstraintQueryRecord]:
        raw = self.connection.execute('CALL db.constraints')
        records = [extract_record_detail(record['detail']) for record in raw]
        return [Neo4jConstraintQueryRecord(**record) for record in records]

    def _convert_constraints(self, raw: List[Neo4jConstraintQueryRecord]) -> ConstraintSet:
        return convert_constraints_with_type_mapper(raw, self.type_mapper)

    def fetch(self) -> ConstraintSet:
        raw: List[Neo4jConstraintQueryRecord] = self._fetch_raw_data()
        constraints: ConstraintSet = self._convert_constraints(raw)
        return constraints
