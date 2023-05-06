import textwrap
from abc import ABC
from typing import List


class Task(ABC):
    """
    A task is responsible for generating a prompt and processing the associated response.
    """

    def prompt(self, query: str) -> str:
        return textwrap.dedent(self.generate_prompt(query))

    def generate_prompt(self, query: str) -> str:
        pass

    def process_response(self, response: str) -> None:
        pass


class TaskResponse:
    next_queries: List[str]

    def __init__(self, next_queries: List[str]) -> None:
        self.next_queries = next_queries
