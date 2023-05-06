from pathlib import Path
from typing import List

from autogpt.commands.base import Command


class ListFiles(Command):
    def __init__(self, path: Path) -> None:
        self.path = path

    def command(self) -> List[str]:
        return ["ls", "-1", str(self.path)]
