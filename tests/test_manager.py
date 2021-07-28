import pytest

from neomodel_constraints.extractor import ExtractorAbstract
from neomodel_constraints.fetcher import ConstraintsFetcherAbstract
from neomodel_constraints import ConstraintSet, UniqueConstraint, ConstraintManager


class DummyExtractor(ExtractorAbstract):
    def __init__(self, results: ConstraintSet):
        self.results: ConstraintSet = results

    def extract(self) -> ConstraintSet:
        return self.results


class DummyFetcher(ConstraintsFetcherAbstract):
    def __init__(self, result: ConstraintSet):
        self.result: ConstraintSet = result

    def _fetch_raw_data(self):  # not used
        pass

    def _convert_constraints(self, raw):  # not used
        pass

    def fetch(self) -> ConstraintSet:
        return self.result


@pytest.mark.unit
def test_get_update_commands():
    create1 = UniqueConstraint(['A', 'B'], ['x'])
    create2 = UniqueConstraint(['C', 'D'], ['p'])

    keep1 = UniqueConstraint(['E'], ['x'])
    keep2 = UniqueConstraint(['E'], ['q'])
    keep3 = UniqueConstraint(['C'], ['p'])
    keep4 = UniqueConstraint(['A'], ['q'])

    drop1 = UniqueConstraint(['C'], ['y'])
    drop2 = UniqueConstraint(['E', 'B'], ['x'])

    extractor = DummyExtractor(ConstraintSet({
        keep1, keep2, keep3, keep4,
        create1, create2,
    }))

    fetcher = DummyFetcher(ConstraintSet({
        keep1, keep2, keep3, keep4,
        drop1, drop2,
    }))

    manager = ConstraintManager(extractor, fetcher)
    commands = manager.get_update_commands()

    c1 = create1.get_create_command()
    c2 = create2.get_create_command()
    d1 = drop1.get_create_command()
    d2 = drop2.get_create_command()

    assert set(commands) == {c1, c2, d1, d2}

    drop_max_index = max([commands.index(d1), commands.index(d2)])
    create_min_index = min([commands.index(c1), commands.index(c2)])
    assert drop_max_index < create_min_index  # drops before creates
