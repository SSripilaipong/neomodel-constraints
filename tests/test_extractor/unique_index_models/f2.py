import neomodel as nm


class FNoUnique(nm.StructuredNode):
    x1 = nm.StringProperty()
    x2 = nm.StringProperty()


class FUniqueIdWithRelation(nm.StructuredNode):
    u1 = nm.UniqueIdProperty()
    x1 = nm.StringProperty()

    r1 = nm.RelationshipTo('M2', 'R1')


class FSubclassWithUniqueString(FUniqueIdWithRelation):
    u2 = nm.StringProperty(unique_index=True)
