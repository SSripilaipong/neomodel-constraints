from typing import List, Iterable

from .abstract import ConstraintAbstract


class ConstraintSet(set):
    def __init__(self, constraints: Iterable[ConstraintAbstract]):
        super().__init__(constraints)

    def get_create_commands(self) -> List[str]:  # TODO
        pass
