from __future__ import annotations

from typing import Dict, TypedDict


class Message:
    role: str
    content: str

    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


class AssistantMessage(Message):
    def __init__(self, content: str) -> None:
        super().__init__("assistant", content)


class SystemMessage(Message):
    def __init__(self, content: str) -> None:
        super().__init__("system", content)


class UserMessage(Message):
    def __init__(self, content: str) -> None:
        super().__init__("user", content)
