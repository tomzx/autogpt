from typing import List

from autogpt.commands.base import Command


class ExecuteContainer(Command):
    def __init__(self, container: str, command: List[str]):
        self._container = container
        self._command = command

    def command(self) -> List[str]:
        return ["docker", "exec", "-it", self._container] + self._command
