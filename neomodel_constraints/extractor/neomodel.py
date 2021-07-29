from typing import Type, Union, Set, Dict, List, Tuple
import importlib

from neomodel import StructuredNode, StructuredRel, Property

from neomodel_constraints.constraint import ConstraintSet, TypeMapperAbstract

from .abstract import ExtractorAbstract
from .data import ExtractedConstraintRecord, ConstraintType


class NeomodelExtractor(ExtractorAbstract):
    def __init__(self, path: str, type_mapper: TypeMapperAbstract, multi_labels: bool = False):
        self.path: str = path
        self.type_mapper: TypeMapperAbstract = type_mapper
        self.multi_labels: bool = multi_labels

    def get_models(self) -> Set[Type[Union[StructuredNode, StructuredRel]]]:
        models = importlib.import_module(self.path)
        results = set()
        for name in dir(models):
            obj = getattr(models, name)
            if isinstance(obj, type) and issubclass(obj, StructuredNode):
                results.add(obj)
        return results

    @staticmethod
    def list_properties(model: Type[StructuredNode]) -> Dict[str, Property]:
        props: List[Tuple[str, Property]] = model.__all_properties__
        return {name: prop for name, prop in props}

    def list_labels(self, model: Type[StructuredNode]) -> Set[str]:
        labels = {model.__label__}
        if self.multi_labels:
            for parent in model.mro():
                if issubclass(parent, StructuredNode) and parent != StructuredNode:
                    labels.add(parent.__label__)
        return labels

    def extract_raw(self, model: Type[StructuredNode]) -> List[ExtractedConstraintRecord]:
        labels = self.list_labels(model)
        props = self.list_properties(model)

        records = []
        for name, prop in props.items():
            if prop.unique_index:
                record = ExtractedConstraintRecord(name=name, type_=ConstraintType.UNIQUE_INDEX, labels=labels)
                records.append(record)
        return records

    def convert_constraints(self, record: ExtractedConstraintRecord) -> ConstraintSet:
        if record.type_ == ConstraintType.UNIQUE_INDEX:
            constraint_type = self.type_mapper.map('UNIQUENESS')
            raw = {
                'labels_or_types': record.labels,
                'properties': [record.name],
            }
            return ConstraintSet({constraint_type.from_raw(raw)})

        raise NotImplementedError()

    def extract(self) -> ConstraintSet:
        models = self.get_models()

        records: List[ExtractedConstraintRecord] = []
        for model in models:
            raw = self.extract_raw(model)
            records.extend(raw)

        constraints = ConstraintSet({})
        for record in records:
            s = self.convert_constraints(record)
            constraints.update(s)

        return constraints
