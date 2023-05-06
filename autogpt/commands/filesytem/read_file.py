from pathlib import Path
from typing import List

from autogpt.commands.base import Command


class ReadFile(Command):
    def __init__(self, file: Path) -> None:
        self.file = file

    def command(self) -> List[str]:
        return ["cat", str(self.file)]
