from typing import Optional

from autogpt.memory.base import Memory


class RAM(Memory):
    def __init__(self, limit: int = -1) -> None:
        # TODO(tom@tomrochette.com): Possibly limit the number of keys we keep
        self._data = {}
        self.limit = limit

    def create(self, key: str, value: str) -> None:
        self.update(key, value)

    def read(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def update(self, key: str, value: str) -> None:
        if key in self._data:
            del self._data[key]
        self._data[key] = value
        to_delete = max(0, len(self._data) - self.limit)
        if self.limit > 0 and to_delete > 0:
            for key in list(self._data.keys())[:to_delete]:
                del self._data[key]

    def delete(self, key: str) -> None:
        del self._data[key]
