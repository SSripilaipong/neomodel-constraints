from typing import Dict, Type
import pytest

from neomodel_constraints import (
    ConstraintsFetcher, DummyConnection, Neo4jConstraintQueryRecord, ConstraintAbstract, ConstraintSet,
)
from neomodel_constraints.constraint import TypeMapperAbstract


class DummyConstraint(ConstraintAbstract):
    def __init__(self, input_data):
        self.input_data = input_data

    def get_create_command(self) -> str:
        pass

    def get_drop_command(self) -> str:
        pass

    def _equals(self, other: 'ConstraintAbstract') -> bool:
        pass

    def _get_data_hash(self) -> int:
        return 1

    @classmethod
    def from_raw(cls, data: Dict) -> 'ConstraintAbstract':
        return DummyConstraint(input_data=data)


class DummyTypeMapper(TypeMapperAbstract):
    def map(self, type_: str) -> Type[ConstraintAbstract]:
        if type_ == 'UNIQUENESS':
            return DummyConstraint
        raise NotImplementedError()


@pytest.mark.unit
def test_fetch_raw_data():
    e = {
        'id': 123,
        'ownedIndexId': 456,
        'entityType': 'NODE',
        'labelsOrTypes': ['Book'],
        'name': 'constraint_1',
        'type': 'UNIQUENESS',
        'properties': ['isbn'],
    }
    connection = DummyConnection([[e]])
    f = ConstraintsFetcher(connection, DummyTypeMapper())

    raw = f._fetch_raw_data()

    assert raw == [Neo4jConstraintQueryRecord(**e)]


@pytest.mark.unit
def test_convert_uniqueness_records_to_constraint_set():
    a = {
        'id': 123,
        'ownedIndexId': 456,
        'entityType': 'NODE',
        'labelsOrTypes': ['Book'],
        'name': 'constraint_1',
        'type': 'UNIQUENESS',
        'properties': ['isbn'],
    }
    b = {
        'id': 456,
        'ownedIndexId': 789,
        'entityType': 'NODE',
        'labelsOrTypes': ['Person'],
        'name': 'constraint_2',
        'type': 'UNIQUENESS',
        'properties': ['fullName'],
    }
    f = ConstraintsFetcher(DummyConnection([]), DummyTypeMapper())

    raw = [Neo4jConstraintQueryRecord(**a), Neo4jConstraintQueryRecord(**b)]
    result = f._convert_constraints(raw)

    assert result == ConstraintSet({DummyConstraint(a), DummyConstraint(b)})


@pytest.mark.unit
def test_fetch():
    a = {
        'id': 123,
        'ownedIndexId': 456,
        'entityType': 'NODE',
        'labelsOrTypes': ['Book'],
        'name': 'constraint_1',
        'type': 'UNIQUENESS',
        'properties': ['isbn'],
    }
    b = {
        'id': 456,
        'ownedIndexId': 789,
        'entityType': 'NODE',
        'labelsOrTypes': ['Person'],
        'name': 'constraint_2',
        'type': 'UNIQUENESS',
        'properties': ['fullName'],
    }
    f = ConstraintsFetcher(DummyConnection([[a, b]]), DummyTypeMapper())
    result = f.fetch()
    assert result == ConstraintSet({DummyConstraint(a), DummyConstraint(b)})
