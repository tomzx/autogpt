import structlog

from autogpt.backends.base import LLMBase, LLMResponse

logger = structlog.getLogger(__name__)


class Debug(LLMBase):
    def query(self, query: str, model: str = "") -> LLMResponse:
        logger.debug("Query", query=query)
        return LLMResponse("- test\n- test\n- more test", 0)
