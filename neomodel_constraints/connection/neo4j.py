from typing import Optional, List, Dict
from neo4j import GraphDatabase, Driver

from .abstract import ConnectionAbstract, DBExecutionError


class Neo4jConnection(ConnectionAbstract):
    def __init__(self, uri: str, user: str, pwd: str, *, db: str = None):
        self.uri: str = uri
        self.user: str = user
        self.pwd: str = pwd
        self.db: str = db

        self.driver: Optional[Driver] = None

    def is_connected(self) -> bool:
        return bool(self.driver)

    def connect(self):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.pwd))

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def execute(self, command: str) -> List[Dict]:
        if not self.driver:
            raise DBExecutionError('Not connected')

        session = None
        try:
            session = self.driver.session(database=self.db) if self.db is not None else self.driver.session()
            response = list(map(dict, session.run(command)))

            return response
        except Exception as e:
            raise DBExecutionError(str(e))
        finally:
            if session is not None:
                session.close()
