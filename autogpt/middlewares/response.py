from typing import List

from autogpt.middlewares.request import Request


class Response:
    response: str
    next_queries: List[Request]
    cost: float

    def __init__(self, response: str, next_queries: List[Request], cost: float) -> None:
        self.response = response
        self.next_queries = next_queries
        self.cost = cost
