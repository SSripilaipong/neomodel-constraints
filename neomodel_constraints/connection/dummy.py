from typing import List, TypeVar, Deque
from collections import deque

from . abstract import ConnectionAbstract


R = TypeVar('R')  # TODO: find out what type it is


class DummyConnection(ConnectionAbstract):
    def __init__(self, results: List[R]):
        self.results: Deque[R] = deque(results)
        self._connected = False

    def execute(self) -> R:
        return self.results.popleft()

    def close(self):
        self._connected = False

    def connect(self):
        self._connected = True

    def is_connected(self):
        return self._connected
