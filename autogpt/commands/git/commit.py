from typing import List

from autogpt.commands.base import Command


class Commit(Command):
    def __init__(self, message: str = "no message") -> None:
        self.message = message

    def command(self) -> List[str]:
        return ["git", "commit", "-m", self.message]
