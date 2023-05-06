from typing import List

from autogpt.commands.base import Command


class ExecutePythonFile(Command):
    def __init__(self, file: str):
        self.file = file

    def command(self) -> List[str]:
        return ["python", self.file]
