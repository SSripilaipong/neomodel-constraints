from .extractor import ExtractorAbstract
from .fetcher import ConstraintsFetcherAbstract


class ConstraintManager:
    def __init__(self, extractor: ExtractorAbstract, fetcher: ConstraintsFetcherAbstract):
        self.extractor: ExtractorAbstract = extractor
        self.fetcher: ConstraintsFetcherAbstract = fetcher

    def get_update_commands(self):
        to_be = self.extractor.extract()
        existing = self.fetcher.fetch()

        to_create = to_be - existing
        to_drop = existing - to_be

        commands = to_drop.get_drop_commands() + to_create.get_create_commands()
        return commands
