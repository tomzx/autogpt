from typing import Callable

from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response


class Middleware:
    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        return next(request)

    def __call__(self, *args, **kwargs):
        return self.handle(args[0], args[1] if len(args) > 1 else None)
