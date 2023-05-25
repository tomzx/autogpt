from typing import List

from autogpt.middlewares.response import Response


class ResponseGraph:
    def __init__(self, nodes: List[Response]) -> None:
        self.nodes = nodes

    def get_output(self) -> Response:
        return self.nodes[-1]
