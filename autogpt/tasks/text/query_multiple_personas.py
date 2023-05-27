from pathlib import Path
from typing import Dict, List, Optional

import yaml

from autogpt import ROOT_DIR
from autogpt.middlewares.next_requests import NextRequests
from autogpt.middlewares.request import Request
from autogpt.tasks.base import Task, TaskResponse

with Path.open(ROOT_DIR / "data" / "personas.yaml") as f:
    personas: List[Dict[str, str]] = yaml.load(f, Loader=yaml.SafeLoader)


class QueryMultiplePersonas(Task):
    name = "query-multiple-personas"

    def generate_prompt(self, query: str) -> str:
        self.query = query
        return ""

    def process_response(self, response: str) -> TaskResponse:
        next_requests = NextRequests()
        for persona in personas:
            next_requests.add(Request(persona["prompt"] + "\n" + self.query, "simple"))
        return TaskResponse(next_requests)
