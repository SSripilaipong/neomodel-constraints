import pytest
from neomodel_constraints.constraint import ConstraintSet, ConstraintAbstract


class DummyConstraint(ConstraintAbstract):
    def __init__(self, a: int, b: int):
        self.a: int = a
        self.b: int = b

    def get_create_command(self) -> str:
        return f'AAAA {self.a} BBBB {self.b}'

    def _equals(self, other: 'ConstraintAbstract') -> bool:
        if not isinstance(other, self.__class__):
            return False

        return all([
            self.a == other.a,
            self.b == other.b,
        ])

    def _get_data_hash(self) -> int:
        return hash(self.a)*2**3 + hash(self.b)*3**3


@pytest.mark.unit
def test_add_new_constraint_to_empty_set():
    s = ConstraintSet([])

    c = DummyConstraint(1, 2)
    s.add(c)

    assert c in s


@pytest.mark.unit
def test_add_new_constraint_to_nonempty_set():
    e = DummyConstraint(1, 2)
    s = ConstraintSet([e])

    c = DummyConstraint(3, 4)
    s.add(c)

    assert c in s
    assert e in s


@pytest.mark.unit
def test_add_duplicated_constraint_to_nonempty_set():
    s = ConstraintSet([DummyConstraint(1, 2), DummyConstraint(3, 4)])

    c = DummyConstraint(3, 4)
    s.add(c)

    assert c in s
    assert len(s) == 2


@pytest.mark.unit
def test_get_create_command_from_empty_set():
    s = ConstraintSet([])
    assert s.get_create_commands() == []


@pytest.mark.unit
def test_get_create_command_from_nonempty_set():
    a = DummyConstraint(1, 2)
    b = DummyConstraint(3, 4)
    s = ConstraintSet([a, b])

    assert s.get_create_commands() == [a, b]
