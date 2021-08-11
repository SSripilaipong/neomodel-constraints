import uuid
from typing import Optional, Set, Dict, Iterable

from .abstract import ConstraintAbstract


class NodeIndexConstraint(ConstraintAbstract):
    def __init__(self, labels: Iterable[str], properties: Iterable[str], *, name: str = None):
        self.labels: Set[str] = set(labels)
        self.properties: Set[str] = set(properties)
        self.name: Optional[str] = name

    def __repr__(self):
        name_expr = '' if not self.name else f', name={repr(self.name)}'
        return f'{self.__class__.__name__}(labels={repr(self.labels)}, properties={repr(self.properties)}{name_expr})'

    def get_create_command(self, *, name=None) -> str:  # TODO
        props = ', '.join([f'n.{p}' for p in self.properties])
        labels_str = ':'.join(list(self.labels))

        if self.name:
            if name:
                raise ValueError(f'Index name already exists: {self.name}')
        elif name:
            self.name = name
        else:
            self.name = 'index_node_' + uuid.uuid4().hex

        return f'CREATE INDEX {self.name} FOR (n:{labels_str}) ON {props}'

    def get_drop_command(self) -> str:  # TODO
        if self.name is None:
            raise ValueError('Index must have a name provided in order to be dropped.')
        return f'DROP INDEX {self.name}'

    def _equals(self, other: ConstraintAbstract) -> bool:  # TODO
        if not isinstance(other, self.__class__):
            return False
        return self.labels == other.labels and self.properties == other.properties

    def _get_data_hash(self) -> int:  # TODO
        labels_hash = sum(hash(e) for e in self.labels)
        props_hash = sum(hash(e) for e in self.properties)

        return labels_hash*2**3 + props_hash*3**3

    @classmethod
    def from_raw(cls, data: Dict) -> 'NodeIndexConstraint':  # TODO
        return cls(labels=data['labels_or_types'], properties=data['properties'],
                   name=data.get('name', None))
