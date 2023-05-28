import asyncio
from typing import Callable

from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response
from autogpt.models import Interaction, Session


class SaveToDatabase(Middleware):
    """
    Save a prompt/response to the database.
    Expects that the database has been initialized.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    async def write_interaction(self, request: Request, response: Response) -> None:
        interaction = Interaction(prompt=request.prompt, response=response.response, session=self.session)
        await interaction.save()

    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        response = next(request)

        asyncio.run(self.write_interaction(request, response))

        return response
