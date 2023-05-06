from autogpt.backends.base import LLMBase, LLMResponse


class Debug(LLMBase):
    def query(self, query: str, model: str = "") -> LLMResponse:
        return LLMResponse("- test\n- test\n- more test", 0)
