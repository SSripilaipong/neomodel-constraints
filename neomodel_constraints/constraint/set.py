from typing import List, Iterable

from .abstract import ConstraintAbstract


class ConstraintSet(set):
    def __init__(self, constraints: Iterable[ConstraintAbstract] = ()):
        super().__init__(constraints)

    def get_create_commands(self) -> List[str]:
        commands = []
        for constraint in self:  # type: ConstraintAbstract
            c = constraint.get_create_command()
            commands.append(c)
        return commands

    def get_drop_commands(self) -> List[str]:
        commands = []
        for constraint in self:  # type: ConstraintAbstract
            c = constraint.get_drop_command()
            commands.append(c)
        return commands

    def difference(self, s: 'ConstraintSet') -> 'ConstraintSet':
        return ConstraintSet(super().difference(*s))

    def union(self, s: 'ConstraintSet') -> 'ConstraintSet':
        return ConstraintSet(super().union(s))

    def __sub__(self, other: 'ConstraintSet') -> 'ConstraintSet':
        return ConstraintSet(super().__sub__(other))

    def __or__(self, other: 'ConstraintSet') -> 'ConstraintSet':
        return ConstraintSet(super().__or__(other))

    def __iter__(self) -> Iterable[ConstraintAbstract]:
        return super(ConstraintSet, self).__iter__()
