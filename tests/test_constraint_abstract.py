from neomodel_constraints.constraint import ConstraintAbstract


class DummyConstraint1(ConstraintAbstract):
    def __init__(self, data_hash: int):
        self.data_hash: int = data_hash

    def get_create_command(self) -> str:  # not used
        return ''

    def _equals(self, other: 'ConstraintAbstract') -> bool:  # not used
        return False

    def _get_data_hash(self) -> int:
        return self.data_hash


class DummyConstraint2(ConstraintAbstract):
    def __init__(self, data_hash: int):
        self.data_hash: int = data_hash

    def get_create_command(self) -> str:  # not used
        return ''

    def _equals(self, other: 'ConstraintAbstract') -> bool:  # not used
        return False

    def _get_data_hash(self) -> int:
        return self.data_hash


class DummyConstraint11(DummyConstraint1):
    pass


def test_hash_same_class_with_same_data_hash():
    c1 = DummyConstraint1(1)
    c2 = DummyConstraint1(1)
    assert hash(c1) == hash(c2)


def test_hash_same_class_with_different_data_hash():
    c1 = DummyConstraint1(1)
    c2 = DummyConstraint1(2)
    assert hash(c1) != hash(c2)


def test_hash_different_class_with_same_data_hash():
    c1 = DummyConstraint1(1)
    c2 = DummyConstraint2(1)
    assert hash(c1) != hash(c2)


def test_hash_different_class_with_different_data_hash():
    c1 = DummyConstraint1(1)
    c2 = DummyConstraint2(2)
    assert hash(c1) != hash(c2)


def test_hash_subclass_with_same_data_hash():
    c1 = DummyConstraint1(1)
    c2 = DummyConstraint11(1)
    assert hash(c1) != hash(c2)


def test_hash_subclass_with_different_data_hash():
    c1 = DummyConstraint1(1)
    c2 = DummyConstraint11(2)
    assert hash(c1) != hash(c2)
