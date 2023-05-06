from typing import List

from autogpt.commands.base import Command


class Add(Command):
    def __init__(self, file: str) -> None:
        self.file = file

    def command(self) -> List[str]:
        return ["git", "add", self.file]
