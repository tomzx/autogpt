# TODO(tom@tomrochette.com): Should the memory be responsible for deciding
# the key to generate?
from abc import ABC


class Memory(ABC):
    def create(self, key: str, value: str) -> None:
        pass

    def read(self, key: str) -> str:
        pass

    def update(self, key: str, value: str) -> None:
        pass

    def delete(self, key: str) -> None:
        pass
