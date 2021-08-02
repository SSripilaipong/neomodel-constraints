from typing import List

from neomodel_constraints.constraint import ConstraintSet, TypeMapperAbstract

from .data import Neo4jConstraintQueryRecord


def convert_constraints_with_type_mapper(
        raw: List[Neo4jConstraintQueryRecord],
        type_mapper: TypeMapperAbstract
) -> ConstraintSet:

    constraints = set()
    for record in raw:
        constraint_type = type_mapper.map(record.type_)
        constraint = constraint_type.from_raw(record.dict())
        constraints.add(constraint)

    return ConstraintSet(constraints)
