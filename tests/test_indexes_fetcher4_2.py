from typing import Dict, Type
import pytest

from neomodel_constraints import (
    DummyConnection, Neo4jIndexQueryRecord, ConstraintAbstract, ConstraintSet,
)
from neomodel_constraints.fetcher.v4_2 import IndexesOnlyFetcher
from neomodel_constraints.constraint import TypeMapperAbstract


raw_columns_rename = {
    'id': 'id_',
    'populationPercent': 'population_percent',
    'type': 'type_',
    'entityType': 'entity_type',
    'labelsOrTypes': 'labels_or_types',
    'indexProvider': 'index_provider',
    'name': 'name',
    'properties': 'properties',
    'state': 'state',
    'uniqueness': 'uniqueness',
}


class DummyConstraint(ConstraintAbstract):
    def __init__(self, input_data):
        self.input_data = input_data

    def get_create_command(self) -> str:
        pass

    def get_drop_command(self) -> str:
        pass

    def __repr__(self):
        return f'DummyConstraint({self.input_data})'

    def _equals(self, other: 'ConstraintAbstract') -> bool:
        if not isinstance(other, DummyConstraint):
            return False
        if self.input_data == other.input_data:
            return True
        return False

    def _get_data_hash(self) -> int:
        return 1

    @classmethod
    def from_raw(cls, data: Dict) -> 'ConstraintAbstract':
        return DummyConstraint(input_data=data)


class DummyTypeMapper(TypeMapperAbstract):
    def map(self, type_: str) -> Type[ConstraintAbstract]:
        if type_ == 'NONUNIQUE_INDEX':
            return DummyConstraint
        raise NotImplementedError()


@pytest.mark.unit
def test_fetch_dummy_raw_data():
    e = {
        'id': 123,
        'entityType': 'NODE',
        'labelsOrTypes': ['Book'],
        'name': 'constraint_1',
        'type': 'BTREE',
        'properties': ['isbn'],
        'populationPercent': 100.0,
        'indexProvider': 'native-btree-1.0',
        'state': 'ONLINE',
        'uniqueness': 'NONUNIQUE',
    }

    connection = DummyConnection([[e]])
    f = IndexesOnlyFetcher(connection, DummyTypeMapper())

    raw = f._fetch_raw_data()

    assert raw == [Neo4jIndexQueryRecord(**e)]


@pytest.mark.unit
def test_fetch_dummy_raw_data_with_lookup_type():
    e = {
        'id': 123,
        'entityType': 'NODE',
        'labelsOrTypes': ['Book'],
        'name': 'constraint_1',
        'type': 'LOOKUP',
        'properties': ['isbn'],
        'populationPercent': 100.0,
        'indexProvider': 'native-btree-1.0',
        'state': 'ONLINE',
        'uniqueness': 'NONUNIQUE',
    }

    connection = DummyConnection([[e]])
    f = IndexesOnlyFetcher(connection, DummyTypeMapper())

    raw = f._fetch_raw_data()

    assert raw == []


@pytest.mark.unit
def test_fetch_dummy_raw_data_with_relationship_entity():
    e = {
        'id': 123,
        'entityType': 'RELATIONSHIP',
        'labelsOrTypes': ['Book'],
        'name': 'constraint_1',
        'type': 'BTREE',
        'properties': ['isbn'],
        'populationPercent': 100.0,
        'indexProvider': 'native-btree-1.0',
        'state': 'ONLINE',
        'uniqueness': 'NONUNIQUE',
    }

    connection = DummyConnection([[e]])
    f = IndexesOnlyFetcher(connection, DummyTypeMapper())

    raw = f._fetch_raw_data()

    assert raw == []


@pytest.mark.unit
def test_fetch_dummy_raw_data_with_unique_constraint():
    e = {
        'id': 123,
        'entityType': 'NODE',
        'labelsOrTypes': ['Book'],
        'name': 'constraint_1',
        'type': 'BTREE',
        'properties': ['isbn'],
        'populationPercent': 100.0,
        'indexProvider': 'native-btree-1.0',
        'state': 'ONLINE',
        'uniqueness': 'UNIQUE',
    }

    connection = DummyConnection([[e]])
    f = IndexesOnlyFetcher(connection, DummyTypeMapper())

    raw = f._fetch_raw_data()

    assert raw == []


@pytest.mark.unit
def test_convert_uniqueness_records_to_constraint_set():
    a = {
        'id': 123,
        'entityType': 'NODE',
        'labelsOrTypes': ['Book'],
        'name': 'constraint_1',
        'type': 'BTREE',
        'properties': ['isbn'],
        'populationPercent': 100.0,
        'indexProvider': 'native-btree-1.0',
        'state': 'ONLINE',
        'uniqueness': 'NONUNIQUE',
    }
    b = {
        'id': 456,
        'entityType': 'NODE',
        'labelsOrTypes': ['Person'],
        'name': 'constraint_2',
        'type': 'BTREE',
        'properties': ['fullName'],
        'populationPercent': 100.0,
        'indexProvider': 'native-btree-1.0',
        'state': 'ONLINE',
        'uniqueness': 'NONUNIQUE',
    }
    f = IndexesOnlyFetcher(DummyConnection([]), DummyTypeMapper())

    raw = [Neo4jIndexQueryRecord(**a), Neo4jIndexQueryRecord(**b)]
    result = f._convert_index(raw)

    a_renamed = {raw_columns_rename[k]: v for k, v in a.items()}
    b_renamed = {raw_columns_rename[k]: v for k, v in b.items()}
    assert result == ConstraintSet({DummyConstraint(a_renamed), DummyConstraint(b_renamed)})


@pytest.mark.unit
def test_fetch():
    a = {
        'id': 123,
        'entityType': 'NODE',
        'labelsOrTypes': ['Book'],
        'name': 'constraint_1',
        'type': 'BTREE',
        'properties': ['isbn'],
        'populationPercent': 100.0,
        'indexProvider': 'native-btree-1.0',
        'state': 'ONLINE',
        'uniqueness': 'NONUNIQUE',
    }
    b = {
        'id': 456,
        'entityType': 'NODE',
        'labelsOrTypes': ['Person'],
        'name': 'constraint_2',
        'type': 'BTREE',
        'properties': ['fullName'],
        'populationPercent': 100.0,
        'indexProvider': 'native-btree-1.0',
        'state': 'ONLINE',
        'uniqueness': 'NONUNIQUE',
    }
    f = IndexesOnlyFetcher(DummyConnection([[a, b]]), DummyTypeMapper())
    result = f.fetch()

    a_renamed = {raw_columns_rename[k]: v for k, v in a.items()}
    b_renamed = {raw_columns_rename[k]: v for k, v in b.items()}
    assert result == ConstraintSet({DummyConstraint(a_renamed), DummyConstraint(b_renamed)})
