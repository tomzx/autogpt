from typing import List

from autogpt.commands.base import Command


class StartContainer(Command):
    def __init__(self, image: str, command: List[str], volumes: List[str]) -> None:
        self._image = image
        self._command = command
        self._volumes = volumes

    def command(self) -> List[str]:
        command = ["docker", "run", "-it"]
        command += [f"-v {volume}" for volume in self._volumes]
        command += [self._image]
        command += self._command
        return command
