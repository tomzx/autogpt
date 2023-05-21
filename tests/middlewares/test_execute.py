from typing import Callable

from autogpt.middlewares.execute import call
from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response


class BeforeMiddleware(Middleware):
    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        request.prompt = "before"
        return next(request)


class AfterMiddleware(Middleware):
    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        response = next(request)
        response.response = "after"
        return response


def test_call():
    middlewares = [
        BeforeMiddleware(),
        AfterMiddleware(),
    ]

    request = Request("test", "simple")
    response = call(middlewares, request)

    assert response
