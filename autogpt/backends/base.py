from abc import ABC


class LLMResponse:
    response: str
    cost: float

    def __init__(self, response: str, cost: float) -> None:
        self.response = response
        self.cost = cost


class LLMBase(ABC):
    def query(self, query: str, model: str = "") -> LLMResponse:
        pass
