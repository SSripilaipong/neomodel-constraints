import neomodel as nm


class UniqueIdAndUniqueString(nm.StructuredNode):
    u1 = nm.UniqueIdProperty()
    u2 = nm.StringProperty(unique_index=True)
    x1 = nm.StringProperty()
