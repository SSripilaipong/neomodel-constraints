from neomodel import *


class FUniqueIdAndUniqueString(StructuredNode):
    u1 = UniqueIdProperty()
    u2 = StringProperty(unique_index=True)
    x1 = StringProperty()
