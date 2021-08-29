import neomodel as nm


class HNotAlone(nm.StructuredNode):
    x1 = nm.StringProperty()
    x2 = nm.StringProperty()


class HNotAloneRelation(nm.StructuredNode):
    x1 = nm.StringProperty()

    r1 = nm.RelationshipTo('M2', 'R1')


class HNotAloneSubclass(HNotAloneRelation):
    x2 = nm.StringProperty()
