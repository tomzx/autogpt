from __future__ import annotations

import inspect
import subprocess
from typing import List


class Command:
    # TODO(tom@tomrochette.com): For the commands to be in the list they need to be loaded
    registry: List[Command] = []

    def __init_subclass__(cls, **kwargs):
        cls.registry += [cls]

    def command(self) -> List[str]:
        return []

    def __call__(self) -> str:
        return subprocess.check_output(self.command(), shell=True).decode("utf-8").strip()

    @classmethod
    def get_signature(cls) -> List[inspect.Parameter]:
        signature = inspect.signature(cls.__init__)
        parameters = list(signature.parameters.values())[1:]
        parameters = [str(parameter) for parameter in parameters]
        signature = inspect.signature(cls.__call__)
        return f"{cls.__name__}({''.join(parameters)}) -> {signature.return_annotation}"

    @classmethod
    def get_command_signatures(cls) -> List[str]:
        # TODO(tom@tomrochette.com): Check to avoid name conflicts
        return [command.get_signature() for command in cls.registry]
