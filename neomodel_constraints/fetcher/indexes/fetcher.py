from typing import Type

from neomodel_constraints.fetcher.indexes import v4_2


IndexesOnlyFetcher = v4_2.IndexesOnlyFetcher


def get_indexes_fetcher(version) -> Type[v4_2.IndexesOnlyFetcher]:
    if version >= ("4", "2", "0"):
        fetcher = v4_2.IndexesOnlyFetcher
    else:
        raise NotImplementedError()
    return fetcher
