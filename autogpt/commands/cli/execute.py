from typing import List

from autogpt.commands.base import Command


class Execute(Command):
    def __init__(self, command: List[str]) -> None:
        self.command = command

    def command(self) -> List[str]:
        return self.command
