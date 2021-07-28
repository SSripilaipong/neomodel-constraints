import neomodel as nm


class NoUnique(nm.StructuredNode):
    x1 = nm.StringProperty()
    x2 = nm.StringProperty()


class UniqueIdWithRelation(nm.StructuredNode):
    u1 = nm.UniqueIdProperty()
    x1 = nm.StringProperty()

    r1 = nm.RelationshipTo('M2', 'R1')


class SubclassWithUniqueString(UniqueIdWithRelation):
    u2 = nm.StringProperty(unique_index=True)
