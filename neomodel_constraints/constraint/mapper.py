from typing import Type

from .abstract import TypeMapperAbstract, ConstraintAbstract
from .unique import UniqueConstraint


class Neo4jConstraintTypeMapper(TypeMapperAbstract):
    def map(self, type_: str) -> Type[ConstraintAbstract]:
        type_ = type_.upper().strip()

        if type_ == 'UNIQUENESS':
            return UniqueConstraint

        raise NotImplementedError(f'type: "{type_}"')
