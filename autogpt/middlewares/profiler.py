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

    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        start_time = time.time()
        time_before_end = start_time
        time_after_start = start_time

        def new_next(request: Request) -> Response:
            nonlocal time_before_end
            nonlocal time_after_start
            time_before_end = time.time()
            response = next(request)
            time_after_start = time.time()
            return response

        response = self.middleware.handle(request, new_next)

        end_time = time.time()

        duration_before = round(time_before_end - start_time, 3)
        duration_after = round(end_time - time_after_start, 3)
        duration = round(duration_before + duration_after, 3)
        total_duration = round(end_time - start_time, 3)
        logger.debug(
            "Profiler",
            name=self.name,
            duration=duration,
            duration_before=duration_before,
            duration_after=duration_after,
            total_duration=total_duration,
        )

        return response
