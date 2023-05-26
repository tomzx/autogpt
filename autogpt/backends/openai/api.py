import time

import structlog
from openai import APIError, ChatCompletion
from tenacity import Retrying, stop_after_delay, wait_exponential

from autogpt.backends.base import LLMBase, LLMResponse
from autogpt.backends.openai.cost_calculator import CostCalculator
from autogpt.backends.openai.message import Message, UserMessage
from autogpt.backends.openai.usage import Usage
from autogpt.errors import QueryExecutionError

logger = structlog.getLogger(__name__)


class Api(LLMBase):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.usage = Usage()

    def query(self, query: str, model: str = "gpt-3.5-turbo") -> LLMResponse:
        # return LLMResponse("test")
        # TODO(tom@tomrochette.com): Handle custom temperature, top_p, n,
        # max_tokens, presence_penalty, frequency_penalty, logit_bias

        self.usage.requests += 1
        try:
            logger.debug("Sending request to OpenAI API", query=query, model=model)
            start_time = time.time()
            for attempt in Retrying(stop=stop_after_delay(30), wait=wait_exponential(1, min=1, max=10)):
                with attempt:
                    response = ChatCompletion.create(
                        api_key=self.api_key,
                        model=model,
                        messages=[
                            UserMessage(query).to_dict(),
                        ],
                        temperature=0.7,
                    )
        except APIError as e:
            raise QueryExecutionError(e)

        content = response.choices[0].message.content

        duration = round(time.time() - start_time)
        logger.debug("Received response from OpenAI API", response=content, duration=duration)
        cost = CostCalculator().calculate(response.usage.total_tokens, model)
        logger.debug("Usage statistics", usage=response.usage.to_dict(), cost=cost)

        # Update usage statistics
        self.usage.completed_requests += 1
        for key, value in response.usage.items():
            setattr(self.usage, key, getattr(self.usage, key) + value)

        return LLMResponse(content, cost)
