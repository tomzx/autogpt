from pathlib import Path
from typing import List

from autogpt.commands.base import Command


class WriteFile(Command):
    def __init__(self, path: Path, content: str) -> None:
        self.path = path
        self.content = content

    def command(self) -> List[str]:
        return ["printf", self.content.replace("\n", "\\n"), ">", str(self.path)]
