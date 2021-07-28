from typing import List, Dict
from abc import ABC, abstractmethod


class ConnectionAbstract(ABC):
    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute(self, command: str) -> List[Dict]:
        pass

    @abstractmethod
    def close(self):
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class DBConnectionError(Exception):
    pass


class DBExecutionError(Exception):
    pass
