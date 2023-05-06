from typing import Callable, List

from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response


def call(middlewares: List[Middleware], request: Request) -> Response:
    def wrapper(
        request: Request, middleware: Middleware, action: Middleware
    ) -> Callable[[Request], Response]:
        return lambda request: middleware(request, action)

    action = lambda request: Response("", [], 0)
    for middleware in middlewares:
        action = wrapper(request, middleware, action)

    return action(request)
