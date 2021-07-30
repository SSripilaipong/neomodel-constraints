from typing import List, Dict, Type
import pytest

from neomodel import UniqueIdProperty, StringProperty

from neomodel_constraints import NeomodelExtractor, ConstraintSet, UniqueConstraint, ConstraintAbstract
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
def test_list_all_models_in_module():
    from tests.test_extractor import models as module

    extractor = NeomodelExtractor('tests.test_extractor.models', DummyTypeMapper())
    models = extractor.get_models(module)
    expected = {'UniqueIdAndUniqueString', 'NoUnique', 'UniqueIdWithRelation',
                'SubclassWithUniqueString', 'NoUniqueAlone'}
    assert {m.__name__ for m in models} == expected


@pytest.mark.unit
def test_get_module():
    from tests.test_extractor import models as expected

    extractor = NeomodelExtractor('tests.test_extractor.models', DummyTypeMapper())
    module = extractor.get_module()
    assert module == expected


@pytest.mark.unit
def test_get_submodule_or_model_module():
    from tests.test_extractor import models as module
    from tests.test_extractor.models import f1 as expected

    extractor = NeomodelExtractor('tests.test_extractor.models:f1', DummyTypeMapper())
    submodule = extractor.get_submodule_or_model(module)
    assert submodule == expected


@pytest.mark.unit
def test_get_submodule_or_model_model():
    from tests.test_extractor import models as module
    from tests.test_extractor.models import UniqueIdAndUniqueString as Expected

    extractor = NeomodelExtractor('tests.test_extractor.models:UniqueIdAndUniqueString', DummyTypeMapper())
    model = extractor.get_submodule_or_model(module)
    assert model == Expected


@pytest.mark.unit
def test_list_props():
    from tests.test_extractor.models.f1 import UniqueIdAndUniqueString

    extractor = NeomodelExtractor('tests.test_extractor.models', DummyTypeMapper())
    properties = extractor.list_properties(UniqueIdAndUniqueString)

    assert set(properties) == {'u1', 'u2', 'x1'}

    u1 = properties['u1']
    u2 = properties['u2']
    x1 = properties['x1']

    assert isinstance(u1, UniqueIdProperty) and u1.unique_index
    assert isinstance(u2, StringProperty) and u2.unique_index
    assert isinstance(x1, StringProperty) and not x1.unique_index


@pytest.mark.unit
def test_list_props_of_subclass():
    from tests.test_extractor.models.f2 import SubclassWithUniqueString

    extractor = NeomodelExtractor('tests.test_extractor.models', DummyTypeMapper())
    properties = extractor.list_properties(SubclassWithUniqueString)

    assert set(properties) == {'u1', 'u2', 'x1'}

    u1 = properties['u1']
    u2 = properties['u2']
    x1 = properties['x1']

    assert isinstance(u1, UniqueIdProperty) and u1.unique_index
    assert isinstance(u2, StringProperty) and u2.unique_index
    assert isinstance(x1, StringProperty) and not x1.unique_index


@pytest.mark.unit
def test_list_labels():
    from tests.test_extractor.models.f1 import UniqueIdAndUniqueString

    extractor = NeomodelExtractor('tests.test_extractor.models', DummyTypeMapper())
    labels = extractor.list_labels(UniqueIdAndUniqueString)
    assert labels == {'UniqueIdAndUniqueString'}


@pytest.mark.unit
def test_list_labels_of_subclass():
    from tests.test_extractor.models.f2 import SubclassWithUniqueString

    extractor = NeomodelExtractor('tests.test_extractor.models', DummyTypeMapper())
    labels = extractor.list_labels(SubclassWithUniqueString)

    assert labels == {'SubclassWithUniqueString'}


@pytest.mark.unit
def test_extract_raw_constraints():
    from tests.test_extractor.models.f1 import UniqueIdAndUniqueString

    extractor = NeomodelExtractor('tests.test_extractor.models', DummyTypeMapper())
    raw_constraints: List[ExtractedConstraintRecord] = extractor.extract_raw(UniqueIdAndUniqueString)

    expected = [
        ExtractedConstraintRecord(type_='UNIQUE_INDEX', labels=['UniqueIdAndUniqueString'], name='u1'),
        ExtractedConstraintRecord(type_='UNIQUE_INDEX', labels=['UniqueIdAndUniqueString'], name='u2'),
    ]

    assert len(raw_constraints) == len(expected)
    for e in expected:
        assert e in raw_constraints


@pytest.mark.unit
def test_convert_unique_index_constraint_record():
    extractor = NeomodelExtractor('tests.test_extractor.models', DummyTypeMapper())
    record = ExtractedConstraintRecord(type_='UNIQUE_INDEX', labels=['UniqueIdAndUniqueString'], name='u1')
    constraints = extractor.convert_constraints(record)

    raw = {'labels_or_types': {'UniqueIdAndUniqueString'}, 'properties': ['u1']}
    assert constraints == ConstraintSet({DummyConstraint(raw)})


@pytest.mark.unit
def test_extract_module():
    extractor = NeomodelExtractor('tests.test_extractor.models', DummyTypeMapper())
    constraints = extractor.extract()

    expected = ConstraintSet({
        DummyConstraint({'labels_or_types': {'UniqueIdAndUniqueString'}, 'properties': ['u1']}),
        DummyConstraint({'labels_or_types': {'UniqueIdAndUniqueString'}, 'properties': ['u2']}),
        DummyConstraint({'labels_or_types': {'UniqueIdWithRelation'}, 'properties': ['u1']}),
        DummyConstraint({'labels_or_types': {'SubclassWithUniqueString'}, 'properties': ['u1']}),
        DummyConstraint({'labels_or_types': {'SubclassWithUniqueString'}, 'properties': ['u2']}),
    })

    assert constraints == expected
