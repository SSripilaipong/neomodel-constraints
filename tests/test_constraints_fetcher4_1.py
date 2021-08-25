from typing import Dict, Type
import pytest

from neomodel_constraints import (
    DummyConnection, Neo4jConstraintQueryRecord, ConstraintAbstract, ConstraintSet,
)
from neomodel_constraints.fetcher.v4_1 import ConstraintsFetcher
from neomodel_constraints.constraint import TypeMapperAbstract


raw_columns_rename = {
    'id': 'id_',
    'ownedIndexId': 'owned_index_id',
    'entityType': 'entity_type',
    'labelsOrTypes': 'labels_or_types',
    'name': 'name',
    'type': 'type_',
    'properties': 'properties',
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
        if type_ == 'UNIQUENESS':
            return DummyConstraint
        raise NotImplementedError()


@pytest.mark.unit
def test_fetch_dummy_raw_data():
    e = {
        'name': 'cstr_unique_35f309fc1791440aa756bb3a2a7d8e52',
        'description': ('CONSTRAINT ON ( subclasswithuniquestring:SubclassWithUniqueString )'
                        'ASSERT (subclasswithuniquestring.u2) IS UNIQUE'),
        'detail': ("Constraint( id=2, name='cstr_unique_35f309fc1791440aa756bb3a2a7d8e52', type='UNIQUENESS', "
                   "schema=(:SubclassWithUniqueString {u2}), ownedIndex=1 )"),
    }
    connection = DummyConnection([[e]])
    f = ConstraintsFetcher(connection, DummyTypeMapper())

    raw = f._fetch_raw_data()

    expected = Neo4jConstraintQueryRecord(id=2, ownedIndexId=1, name='cstr_unique_35f309fc1791440aa756bb3a2a7d8e52',
                                          entityType='NODE', labelsOrTypes=['SubclassWithUniqueString'],
                                          properties=['u2'], type='UNIQUENESS')
    assert raw == [expected]


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

    a_renamed = {raw_columns_rename[k]: v for k, v in a.items()}
    b_renamed = {raw_columns_rename[k]: v for k, v in b.items()}
    assert result == ConstraintSet({DummyConstraint(a_renamed), DummyConstraint(b_renamed)})


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
    ae = {
        'name': a['name'],
        'description': (f'CONSTRAINT ON ( n:{a["labelsOrTypes"][0]} )'
                        f'ASSERT (n.{a["properties"][0]}) IS UNIQUE'),
        'detail': (f"Constraint( id={a['id']}, name='{a['name']}', type='{a['type']}', "
                   f"schema=(:{a['labelsOrTypes'][0]} {{{a['properties'][0]}}}), ownedIndex={a['ownedIndexId']} )"),
    }
    be = {
        'name': b['name'],
        'description': (f'CONSTRAINT ON ( n:{b["labelsOrTypes"][0]} )'
                        f'ASSERT (n.{b["properties"][0]}) IS UNIQUE'),
        'detail': (f"Constraint( id={b['id']}, name='{b['name']}', type='{b['type']}', "
                   f"schema=(:{b['labelsOrTypes'][0]} {{{b['properties'][0]}}}), ownedIndex={b['ownedIndexId']} )"),
    }
    f = ConstraintsFetcher(DummyConnection([[ae, be]]), DummyTypeMapper())
    result = f.fetch()

    a_renamed = {raw_columns_rename[k]: v for k, v in a.items()}
    b_renamed = {raw_columns_rename[k]: v for k, v in b.items()}
    assert result == ConstraintSet({DummyConstraint(a_renamed), DummyConstraint(b_renamed)})
