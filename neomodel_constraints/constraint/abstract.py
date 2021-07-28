from typing import Type, Dict
from abc import ABC, abstractmethod


class ConstraintAbstract(ABC):
    @abstractmethod
    def get_create_command(self) -> str:
        pass

    @abstractmethod
    def get_drop_command(self) -> str:
        pass

    @abstractmethod
    def _equals(self, other: 'ConstraintAbstract') -> bool:
        pass

    @classmethod
    @abstractmethod
    def from_raw(cls, data: Dict) -> 'ConstraintAbstract':
        pass

    @abstractmethod
    def _get_data_hash(self) -> int:
        pass

    def __eq__(self, other: 'ConstraintAbstract') -> bool:
        return self._equals(other)

    def __hash__(self) -> int:
        return hash(self.__class__) + self._get_data_hash()


class TypeMapperAbstract(ABC):
    @abstractmethod
    def map(self, type_: str) -> Type[ConstraintAbstract]:
        pass
