from typing import Union, Type

from . import v4_2, v4_1


ConstraintsFetcher = v4_2.ConstraintsFetcher


def get_constraints_fetcher(version) -> Union[Type[v4_2.ConstraintsFetcher], Type[v4_1.ConstraintsFetcher]]:
    if version >= ("4", "2", "0"):
        fetcher = v4_2.ConstraintsFetcher
    else:
        fetcher = v4_1.ConstraintsFetcher
    return fetcher
