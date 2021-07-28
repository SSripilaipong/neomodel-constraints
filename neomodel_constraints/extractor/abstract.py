from abc import ABC, abstractmethod

from neomodel_constraints.constraint import ConstraintSet


class ExtractorAbstract(ABC):
    @abstractmethod
    def extract(self) -> ConstraintSet:
        pass
