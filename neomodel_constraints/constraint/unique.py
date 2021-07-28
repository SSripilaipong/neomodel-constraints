from typing import List, Optional, Dict

from .abstract import ConstraintAbstract


class UniqueConstraint(ConstraintAbstract):
    def __init__(self, labels: List[str], properties: List[str], *, name: str = None):
        self.labels: List[str] = labels
        self.properties: List[str] = properties
        self.name: Optional[str] = name

    def get_create_command(self) -> str:  # TODO
        """
        CREATE CONSTRAINT {NAME} ON (n:{LABELS}) ASSERT n.{PROPERTIES} IS UNIQUE
        """

    def _equals(self, other: 'ConstraintAbstract') -> bool:  # TODO
        pass

    def _get_data_hash(self) -> int:  # TODO
        pass

    @classmethod  # TODO
    def from_raw(cls, data: Dict) -> 'ConstraintAbstract':
        pass

