from typing import List, Iterable

from .abstract import ConstraintAbstract


class ConstraintSet(set):
    def __init__(self, constraints: Iterable[ConstraintAbstract]):
        super().__init__(constraints)

    def get_create_commands(self) -> List[str]:  # TODO
        pass

    def get_drop_commands(self) -> List[str]:  # TODO
        pass

    def difference(self, s: 'ConstraintSet') -> 'ConstraintSet':
        return ConstraintSet(super().difference(*s))

    def union(self, s: 'ConstraintSet') -> 'ConstraintSet':
        return ConstraintSet(super().union(s))

    def __sub__(self, other: 'ConstraintSet') -> 'ConstraintSet':
        return ConstraintSet(super().__sub__(other))

    def __or__(self, other: 'ConstraintSet') -> 'ConstraintSet':
        return ConstraintSet(super().__or__(other))
