from typing import Type

from .abstract import TypeMapperAbstract, ConstraintAbstract
from .unique import UniqueConstraint
from .node_index import NodeIndexConstraint


class Neo4jConstraintTypeMapper(TypeMapperAbstract):
    def map(self, type_: str) -> Type[ConstraintAbstract]:
        type_ = type_.upper().strip()

        if type_ == 'UNIQUENESS':
            return UniqueConstraint
        elif type_ == 'NODE_INDEX':
            return NodeIndexConstraint

        raise NotImplementedError(f'type: "{type_}"')
