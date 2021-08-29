from typing import List, Dict, Type
import pytest

from neomodel import IntegerProperty, StringProperty

from neomodel_constraints import NeomodelExtractor, ConstraintSet, ConstraintAbstract
from neomodel_constraints.constraint import TypeMapperAbstract
from neomodel_constraints.extractor.data import ExtractedConstraintRecord


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
        return 42

    @classmethod
    def from_raw(cls, data: Dict) -> 'ConstraintAbstract':
        return DummyConstraint(input_data=data)


class DummyTypeMapper(TypeMapperAbstract):
    def map(self, type_: str) -> Type[ConstraintAbstract]:
        # if type_ == 'UNIQUENESS':
        #     return DummyConstraint
        if type_ == 'NONUNIQUE_INDEX':
            return DummyConstraint
        raise NotImplementedError()


@pytest.mark.unit
def test_list_props():
    from tests.test_extractor.index_only_models.g1 import GIntIndexAndStringIndex

    extractor = NeomodelExtractor('tests.test_extractor.index_only_models', DummyTypeMapper())
    properties = extractor.list_properties(GIntIndexAndStringIndex)

    assert set(properties) == {'i1', 'i2', 'x1'}

    i1 = properties['i1']
    i2 = properties['i2']
    x1 = properties['x1']

    assert isinstance(i1, IntegerProperty) and i1.index
    assert isinstance(i2, StringProperty) and i2.index
    assert isinstance(x1, StringProperty) and not x1.index


@pytest.mark.unit
def test_list_props_of_subclass():
    from tests.test_extractor.index_only_models.g2 import GSubclassWithStringIndex

    extractor = NeomodelExtractor('tests.test_extractor.index_only_models', DummyTypeMapper())
    properties = extractor.list_properties(GSubclassWithStringIndex)

    assert set(properties) == {'i1', 'i2', 'x1'}

    i1 = properties['i1']
    i2 = properties['i2']
    x1 = properties['x1']

    assert isinstance(i1, StringProperty) and i1.index
    assert isinstance(i2, StringProperty) and i2.index
    assert isinstance(x1, StringProperty) and not x1.index


@pytest.mark.unit
def test_extract_raw_constraints():
    from tests.test_extractor.index_only_models.g1 import GIntIndexAndStringIndex

    extractor = NeomodelExtractor('tests.test_extractor.index_only_models', DummyTypeMapper())
    raw_constraints: List[ExtractedConstraintRecord] = extractor.extract_raw(GIntIndexAndStringIndex)

    expected = [
        ExtractedConstraintRecord(type_='INDEX_ONLY', labels=['GIntIndexAndStringIndex'], name='i1'),
        ExtractedConstraintRecord(type_='INDEX_ONLY', labels=['GIntIndexAndStringIndex'], name='i2'),
    ]

    assert len(raw_constraints) == len(expected)
    for e in expected:
        assert e in raw_constraints


@pytest.mark.unit
def test_convert_index_only_constraint_record():
    extractor = NeomodelExtractor('tests.test_extractor.index_only_models', DummyTypeMapper())
    record = ExtractedConstraintRecord(type_='INDEX_ONLY', labels=['GUniqueIdAndUniqueString'], name='u1')
    constraints = extractor.convert_constraints(record)

    raw = {'labels_or_types': {'GUniqueIdAndUniqueString'}, 'properties': ['u1']}
    assert constraints == ConstraintSet({DummyConstraint(raw)})


@pytest.mark.unit
def test_extract_module():
    extractor = NeomodelExtractor('tests.test_extractor.index_only_models', DummyTypeMapper())
    constraints = extractor.extract()

    expected = ConstraintSet({
        DummyConstraint({'labels_or_types': {'GIntIndexAndStringIndex'}, 'properties': ['i1']}),
        DummyConstraint({'labels_or_types': {'GIntIndexAndStringIndex'}, 'properties': ['i2']}),
        DummyConstraint({'labels_or_types': {'GStringIndexWithRelation'}, 'properties': ['i1']}),
        DummyConstraint({'labels_or_types': {'GSubclassWithStringIndex'}, 'properties': ['i1']}),
        DummyConstraint({'labels_or_types': {'GSubclassWithStringIndex'}, 'properties': ['i2']}),
    })

    assert constraints == expected
