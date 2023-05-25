from __future__ import annotations

from typing import List, Optional

from autogpt.middlewares.request import Request


class RequestGraphNode:
    def __init__(self, request: Request, needs: List[RequestGraphNode]) -> None:
        self.request = request
        self.needs = needs


class RequestGraph:
    def __init__(self) -> None:
        self.nodes = []

    def add(self, request: Request, needs: Optional[List[RequestGraphNode]] = None) -> RequestGraphNode:
        """
        Assumes that users are adding requests in order, where the needs come from requests previously
        added to the graph.
        The last request added to the graph acts as output for the graph.
        """
        if needs is None:
            needs = []

        node = RequestGraphNode(request, needs)
        self.nodes += [node]

        return node

    def __eq__(self, other):
        return self.nodes == other.nodes
