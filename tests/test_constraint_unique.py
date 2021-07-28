import pytest

from neomodel_constraints import ConstraintAbstract
from neomodel_constraints.constraint.unique import UniqueConstraint


@pytest.mark.unit
def test_equals_another_unique_with_same_data_same_name():
    c1 = UniqueConstraint(['A', 'B'], ['x', 'y'], name='C')
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'], name='C')

    assert c1 == c2


@pytest.mark.unit
def test_hash_another_unique_with_same_data_same_name():
    c1 = UniqueConstraint(['A', 'B'], ['x', 'y'], name='C')
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'], name='C')

    assert hash(c1) == hash(c2)


@pytest.mark.unit
def test_equals_another_unique_with_same_data_different_name():
    c1 = UniqueConstraint(['A', 'B'], ['x', 'y'], name='C')
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'], name='D')

    assert c1 == c2


@pytest.mark.unit
def test_hash_another_unique_with_same_data_different_name():
    c1 = UniqueConstraint(['A', 'B'], ['x', 'y'], name='C')
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'], name='D')

    assert hash(c1) == hash(c2)


@pytest.mark.unit
def test_equals_another_unique_with_same_data_with_one_having_no_name():
    c1 = UniqueConstraint(['A', 'B'], ['x', 'y'], name='C')
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'])

    assert c1 == c2


@pytest.mark.unit
def test_hash_another_unique_with_same_data_with_one_having_no_name():
    c1 = UniqueConstraint(['A', 'B'], ['x', 'y'], name='C')
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'])

    assert hash(c1) == hash(c2)


@pytest.mark.unit
def test_equals_another_unique_with_same_data_both_no_name():
    c1 = UniqueConstraint(['A', 'B'], ['x', 'y'])
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'])

    assert c1 == c2


@pytest.mark.unit
def test_hash_another_unique_with_same_data_both_no_name():
    c1 = UniqueConstraint(['A', 'B'], ['x', 'y'])
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'])

    assert hash(c1) == hash(c2)


@pytest.mark.unit
def test_equals_another_unique_with_same_props_different_labels():
    c1 = UniqueConstraint(['A'], ['x', 'y'])
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'])

    assert c1 != c2


@pytest.mark.unit
def test_hash_another_unique_with_same_props_different_labels():
    c1 = UniqueConstraint(['A'], ['x', 'y'])
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'])

    assert hash(c1) != hash(c2)


@pytest.mark.unit
def test_equals_another_unique_with_same_labels_different_props():
    c1 = UniqueConstraint(['A', 'B'], ['x'])
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'])

    assert c1 != c2


@pytest.mark.unit
def test_hash_another_unique_with_same_labels_different_props():
    c1 = UniqueConstraint(['A', 'B'], ['x'])
    c2 = UniqueConstraint(['A', 'B'], ['x', 'y'])

    assert hash(c1) != hash(c2)


class DummyConstraint(ConstraintAbstract):
    def __init__(self, labels, properties, name=None):
        self.labels = set(labels)
        self.properties = set(properties)
        self.name = name

    get_create_command = UniqueConstraint.get_create_command
    get_drop_command = UniqueConstraint.get_drop_command
    _equals = UniqueConstraint._equals
    _get_data_hash = UniqueConstraint._get_data_hash
    from_raw = UniqueConstraint.from_raw


@pytest.mark.unit
def test_equals_dummy_with_same_data():
    c1 = UniqueConstraint(['A', 'B'], ['x', 'y'])
    c2 = DummyConstraint(['A', 'B'], ['x', 'y'])

    assert c1 != c2


@pytest.mark.unit
def test_hash_dummy_with_same_data():
    c1 = UniqueConstraint(['A', 'B'], ['x', 'y'])
    c2 = DummyConstraint(['A', 'B'], ['x', 'y'])

    assert hash(c1) != hash(c2)
