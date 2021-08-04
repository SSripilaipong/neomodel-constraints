from typing import Union, Type

from .v4_2 import ConstraintsFetcherV4s2
from .v4_1 import ConstraintsFetcherV4s1


ConstraintsFetcher = ConstraintsFetcherV4s2


def get_constraints_fetcher(version) -> Union[Type[ConstraintsFetcherV4s2], Type[ConstraintsFetcherV4s1]]:
    if version >= ("4", "2", "0"):
        fetcher = ConstraintsFetcherV4s2
    else:
        fetcher = ConstraintsFetcherV4s1
    return fetcher
