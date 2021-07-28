import pytest
from neomodel_constraints import Neo4jConstraintTypeMapper, UniqueConstraint


@pytest.mark.unit
def test_map_uniqueness_type():
    mapper = Neo4jConstraintTypeMapper()
    assert mapper.map('UNIQUENESS') == UniqueConstraint
