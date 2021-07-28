from typing import Type, Union, Set, Dict, List
from neomodel import StructuredNode, StructuredRel, Property

from neomodel_constraints.constraint import ConstraintSet

from .abstract import ExtractorAbstract
from .data import ExtractedConstraintRecord


class NeomodelExtractor(ExtractorAbstract):
    def __init__(self, path: str):
        self.path: str = path

    def get_models(self) -> Set[Type[Union[StructuredNode, StructuredRel]]]:  # TODO
        pass

    def list_properties(self, model: Type[StructuredNode]) -> Dict[str, Property]:  # TODO
        pass

    def list_labels(self, model: Type[StructuredNode]) -> Set[str]:  # TODO
        pass

    def extract_raw(self, model: Type[StructuredNode]) -> List[ExtractedConstraintRecord]:  # TODO
        pass

    def convert_constraints(self, record: ExtractedConstraintRecord) -> ConstraintSet:  # TODO
        pass

    def extract(self) -> ConstraintSet:  # TODO
        pass
