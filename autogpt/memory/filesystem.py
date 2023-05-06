from pathlib import Path
from typing import Optional

from autogpt.memory.base import Memory


class FileSystem(Memory):
    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def create(self, key: str, value: str) -> None:
        return self.update(key, value)

    def read(self, key: str) -> Optional[str]:
        with (self.path / key).open() as f:
            return f.read()

    def update(self, key: str, value: str) -> None:
        with (self.path / key).open("w") as f:
            f.write(value)

    def delete(self, key: str) -> None:
        (self.path / key).unlink(missing_ok=True)
