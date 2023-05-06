import shutil
import tempfile
from pathlib import Path


class Workspace:
    def __init__(self) -> None:
        self.directories = []

    def create(self) -> Path:
        directory = Path(tempfile.mkdtemp())
        self.directories += [directory]
        return directory

    def __del__(self) -> None:
        for directory in self.directories:
            shutil.rmtree(directory)
