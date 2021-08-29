from typing import Type, Union

from neomodel_constraints.fetcher.indexes import v4_2
from neomodel_constraints.fetcher.indexes import v4_1


IndexesOnlyFetcher = v4_2.IndexesOnlyFetcher


def get_indexes_fetcher(version) -> Union[Type[v4_2.IndexesOnlyFetcher], Type[v4_1.IndexesOnlyFetcher]]:
    if version >= ("4", "2", "0"):
        fetcher = v4_2.IndexesOnlyFetcher
    else:
        fetcher = v4_1.IndexesOnlyFetcher
    return fetcher
