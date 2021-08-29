import neomodel as nm


class GNoIndex(nm.StructuredNode):
    x1 = nm.StringProperty()
    x2 = nm.StringProperty()


class GStringIndexWithRelation(nm.StructuredNode):
    i1 = nm.StringProperty(index=True)
    x1 = nm.StringProperty()

    r1 = nm.RelationshipTo('M2', 'R1')


class GSubclassWithStringIndex(GStringIndexWithRelation):
    i2 = nm.StringProperty(index=True)
