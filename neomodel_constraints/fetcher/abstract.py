from abc import ABC, abstractmethod

from neomodel_constraints.constraint.set import ConstraintSet


class ConstraintsFetcherAbstract(ABC):
    @abstractmethod
    def fetch(self) -> ConstraintSet:
        pass
