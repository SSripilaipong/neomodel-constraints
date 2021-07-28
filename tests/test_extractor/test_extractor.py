from typing import List
import pytest

from neomodel import UniqueIdProperty, StringProperty

from neomodel_constraints import NeomodelExtractor, ConstraintSet, UniqueConstraint
from neomodel_constraints.extractor.data import ExtractedConstraintRecord


@pytest.mark.unit
def test_list_all_models_in_module():
    extractor = NeomodelExtractor('tests.test_extractor.models')
    models = extractor.get_models()
    expected = {'UniqueIdAndUniqueString', 'NoUnique', 'UniqueIdWithRelation',
                'SubclassWithUniqueString', 'NoUniqueAlone'}
    assert {m.__name__ for m in models} == expected


@pytest.mark.unit
def test_list_props():
    from tests.test_extractor.models.f1 import UniqueIdAndUniqueString

    extractor = NeomodelExtractor('tests.test_extractor.models')
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

    extractor = NeomodelExtractor('tests.test_extractor.models')
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

    extractor = NeomodelExtractor('tests.test_extractor.models')
    labels = extractor.list_labels(UniqueIdAndUniqueString)
    assert labels == {'UniqueIdAndUniqueString'}


@pytest.mark.unit
def test_list_labels_of_subclass():
    from tests.test_extractor.models.f2 import SubclassWithUniqueString

    extractor = NeomodelExtractor('tests.test_extractor.models')
    labels = extractor.list_labels(SubclassWithUniqueString)

    assert labels == {'SubclassWithUniqueString', 'UniqueIdWithRelation'}


@pytest.mark.unit
def test_extract_raw_constraints():
    from tests.test_extractor.models.f1 import UniqueIdAndUniqueString

    extractor = NeomodelExtractor('tests.test_extractor.models')
    raw_constraints: List[ExtractedConstraintRecord] = extractor.extract_raw(UniqueIdAndUniqueString)

    expected = {
        ExtractedConstraintRecord(type_='UNIQUE_INDEX', labels=['UniqueIdAndUniqueString'], name='u1'),
        ExtractedConstraintRecord(type_='UNIQUE_INDEX', labels=['UniqueIdAndUniqueString'], name='u2'),
    }

    assert len(raw_constraints) == len(expected)
    for e in expected:
        assert e in raw_constraints


@pytest.mark.unit
def test_convert_unique_index_constraint_record():
    extractor = NeomodelExtractor('tests.test_extractor.models')
    record = ExtractedConstraintRecord(type_='UNIQUE_INDEX', labels=['UniqueIdAndUniqueString'], name='u1')
    constraints = extractor.convert_constraints(record)
    assert constraints == ConstraintSet({UniqueConstraint({'UniqueIdAndUniqueString'}, {'u1'})})


@pytest.mark.unit
def test_extract_module():
    extractor = NeomodelExtractor('tests.test_extractor.models')
    constraints = extractor.extract()

    expected = ConstraintSet({
        UniqueConstraint({'UniqueIdAndUniqueString'}, {'u1'}),
        UniqueConstraint({'UniqueIdAndUniqueString'}, {'u2'}),
        UniqueConstraint({'UniqueIdWithRelation'}, {'u1'}),
        UniqueConstraint({'SubclassWithUniqueString', 'UniqueIdWithRelation'}, {'u1'}),
        UniqueConstraint({'SubclassWithUniqueString', 'UniqueIdWithRelation'}, {'u2'}),
    })

    assert constraints == expected
