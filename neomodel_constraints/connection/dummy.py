from typing import List, TypeVar, Deque
from collections import deque

from . abstract import ConnectionAbstract


R = TypeVar('R')  # TODO: find out what type it is


class DummyConnection(ConnectionAbstract):
    def __init__(self, results: List[R]):
        self.results: Deque[R] = deque(results)

    def execute(self) -> R:
        return self.results.popleft()

    def close(self):
        pass

    def connect(self):
        pass
