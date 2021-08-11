from typing import List

from .constraint import ConstraintSet
from .extractor import ExtractorAbstract
from .fetcher import FetcherAbstract


class ConstraintManager:
    def __init__(self, extractor: ExtractorAbstract, fetchers: List[FetcherAbstract]):
        self.extractor: ExtractorAbstract = extractor
        self.fetchers: List[FetcherAbstract] = fetchers

    def get_update_commands(self):
        to_be = self.extractor.extract()

        existing = ConstraintSet()
        for fetcher in self.fetchers:
            existing |= fetcher.fetch()

        to_create = to_be - existing
        to_drop = existing - to_be

        commands = to_drop.get_drop_commands() + to_create.get_create_commands()
        return commands
