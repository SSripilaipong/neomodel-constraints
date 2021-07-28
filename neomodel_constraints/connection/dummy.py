from typing import List, Deque, Dict
from collections import deque

from .abstract import ConnectionAbstract


class DummyConnection(ConnectionAbstract):
    def __init__(self, results: List[List[Dict]]):
        self.results: Deque[List[Dict]] = deque(results)
        self._connected = False

    def execute(self, command: str) -> List[Dict]:
        if len(self.results) == 0:
            raise IndexError('No results set')
        return self.results.popleft()

    def close(self):
        self._connected = False

    def connect(self):
        self._connected = True

    def is_connected(self) -> bool:
        return self._connected
