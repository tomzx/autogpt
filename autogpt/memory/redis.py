from typing import Optional

import redis as r

from autogpt.memory.base import Memory


class Redis(Memory):
    def __init__(self, host: str, port: int, database: int) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.client = r.Redis(host=self.host, port=self.port, db=self.database)

    def create(self, key: str, value: str) -> None:
        self.client.update(key, value)

    def read(self, key: str) -> Optional[str]:
        return self.client.get(key)

    def update(self, key: str, value: str) -> None:
        # TODO(tom@tomrochette.com): Look into setting values with an expiration
        self.client.set(key, value)

    def delete(self, key: str) -> None:
        self.client.delete(key)
