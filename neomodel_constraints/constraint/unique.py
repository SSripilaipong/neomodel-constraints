from typing import Optional, Set, Dict, Iterable

from .abstract import ConstraintAbstract


class UniqueConstraint(ConstraintAbstract):
    def __init__(self, labels: Iterable[str], properties: Iterable[str], *, name: str = None):
        self.labels: Set[str] = set(labels)
        self.properties: Set[str] = set(properties)
        self.name: Optional[str] = name

    def get_create_command(self) -> str:  # TODO
        """
        CREATE CONSTRAINT {NAME} ON (n:{LABELS}) ASSERT n.{PROPERTIES} IS UNIQUE
        """

    def get_drop_command(self) -> str:  # TODO
        """
        DROP CONSTRAINT {NAME}
        """

    def _equals(self, other: 'ConstraintAbstract') -> bool:  # TODO
        pass

    def _get_data_hash(self) -> int:  # TODO
        pass

    @classmethod  # TODO
    def from_raw(cls, data: Dict) -> 'ConstraintAbstract':
        pass
