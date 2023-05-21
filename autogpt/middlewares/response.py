from typing import List

from autogpt.middlewares.request import Request


class Response:
    response: str
    next_requests: List[Request]
    cost: float

    def __init__(
        self, response: str, next_requests: List[Request], cost: float
    ) -> None:
        self.response = response
        self.next_requests = next_requests
        self.cost = cost
