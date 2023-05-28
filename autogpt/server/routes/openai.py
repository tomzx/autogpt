from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from autogpt.backends.openai.api import Api
from autogpt.backends.openai.message import Message
from autogpt.configuration.configuration import Configuration

router = APIRouter(prefix="/openai")

api = Api(Configuration.open_api_key)


class CompletionsRequest(BaseModel):
    messages: List[Message]
    model: str = "gpt-3.5-turbo"


@router.post("/v1/chat/completions")
def completions(request: CompletionsRequest):
    return api.completions(request.messages, request.model)
