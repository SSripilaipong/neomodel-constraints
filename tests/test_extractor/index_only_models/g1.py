from neomodel import *


class GIntIndexAndStringIndex(StructuredNode):
    i1 = IntegerProperty(index=True)
    i2 = StringProperty(index=True)
    x1 = StringProperty()
