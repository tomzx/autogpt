import asyncio
from typing import Optional

from autogpt.memory.base import Memory
from autogpt.models.memory import Memory as MemoryModel


class SQL(Memory):
    """
    Expects that the database has been initialized.
    """

    def create(self, key: str, value: str) -> None:
        return self.update(key, value)

    def read(self, key: str) -> Optional[str]:
        return asyncio.run(self._read(key))

    async def _read(self, key: str) -> Optional[str]:
        return await MemoryModel.filter(key=key).first().value

    def update(self, key: str, value: str) -> None:
        asyncio.run(self._update(key, value))

    async def _update(self, key: str, value: str) -> None:
        await MemoryModel(key=key, value=value).update_or_create()

    def delete(self, key: str) -> None:
        asyncio.run(self._delete(key))

    async def _delete(self, key: str) -> None:
        await Memory.filter(key=key).delete()
