from autogpt.backends.base import LLMBase, LLMResponse
from autogpt.middlewares.call_llm import CallLLM
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response


class TestLLMBase(LLMBase):
    def query(self, query: str, model: str = "") -> LLMResponse:
        return LLMResponse("", 0)


def test_call_llm():
    assert CallLLM(TestLLMBase()).handle(Request("test", "simple"), None) == Response(
        "", [], 0
    )
