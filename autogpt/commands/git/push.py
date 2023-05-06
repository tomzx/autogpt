from typing import List

from autogpt.commands.base import Command


class Push(Command):
    def command(self) -> List[str]:
        return ["git", "push"]
