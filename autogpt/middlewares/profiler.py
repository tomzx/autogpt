import time
from typing import Callable

import structlog

from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response

logger = structlog.get_logger(__name__)


class Profiler(Middleware):
    def __init__(self, middleware: Middleware) -> None:
        self.middleware = middleware
        self.name = self.middleware.__class__.__name__
        self.duration = 0
        # self.measurements: Dict[str, float] = {}

    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        start_time = time.time()

        # response = next(request)
        response = self.middleware.handle(request, next)

        end_time = time.time()

        self.duration = round(end_time - start_time, 3)
        logger.debug("Profiler", name=self.name, duration=self.duration)

        return response
