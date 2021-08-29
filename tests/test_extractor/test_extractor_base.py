from typing import List, Dict, Type
import pytest

from neomodel import IntegerProperty, StringProperty

from neomodel_constraints import NeomodelExtractor, ConstraintAbstract
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
        return DummyConstraint


@pytest.mark.unit
def test_list_props():
    from tests.test_extractor.basic_models.h1 import HAlone

    extractor = NeomodelExtractor('tests.test_extractor.basic_models', DummyTypeMapper())
    properties = extractor.list_properties(HAlone)

    assert set(properties) == {'x1', 'x2'}

    x1 = properties['x1']
    x2 = properties['x2']

    assert isinstance(x1, IntegerProperty)
    assert isinstance(x2, StringProperty)


@pytest.mark.unit
def test_list_props_of_subclass():
    from tests.test_extractor.basic_models.h2 import HNotAloneSubclass

    extractor = NeomodelExtractor('tests.test_extractor.basic_models', DummyTypeMapper())
    properties = extractor.list_properties(HNotAloneSubclass)

    assert set(properties) == {'x1', 'x2'}

    x1 = properties['x1']
    x2 = properties['x2']

    assert isinstance(x1, StringProperty) and not x1.index
    assert isinstance(x2, StringProperty) and not x2.index


@pytest.mark.unit
def test_extract_raw_constraints():
    from tests.test_extractor.basic_models.h1 import HAlone

    extractor = NeomodelExtractor('tests.test_extractor.basic_models.h1', DummyTypeMapper())
    raw_constraints: List[ExtractedConstraintRecord] = extractor.extract_raw(HAlone)

    assert len(raw_constraints) == 0
