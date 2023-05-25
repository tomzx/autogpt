from autogpt.tasks.next_requests import NextRequests


class Response:
    response: str
    next_requests: NextRequests
    cost: float

    def __init__(self, response: str, next_requests: NextRequests, cost: float) -> None:
        self.response = response
        self.next_requests = next_requests
        self.cost = cost

    def __eq__(self, other):
        return self.response == other.response and self.next_requests == other.next_requests and self.cost == other.cost
