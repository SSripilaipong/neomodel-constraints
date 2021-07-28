from abc import ABC, abstractmethod


class ConstraintAbstract(ABC):
    @abstractmethod
    def get_create_command(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, other: 'Constraint') -> bool:
        pass

    @abstractmethod
    def _get_data_hash(self) -> int:
        pass

    def __hash__(self) -> int:
        return hash(self.__class__) + self._get_data_hash()
