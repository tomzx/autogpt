import asyncio

import structlog

from autogpt import models
from autogpt.backends.openai.message import Message

logger = structlog.get_logger(__name__)


class Session:
    def start(self) -> None:
        self.messages = []
        # self.session = models.Session()
        # asyncio.run(self.session.save())
        # logger.debug("Session started", session_id=self.session.id)
        logger.debug("Session started")

    def end(self) -> None:
        # asyncio.run(self.session.save())
        logger.debug("Session ended")

    def model(self) -> models.Session:
        return self.session

    def add_message(self, message: Message) -> None:
        self.messages += [message]
