from pathlib import Path
from typing import Dict, List

import yaml

from autogpt import ROOT_DIR
from autogpt.middlewares.request import Request
from autogpt.tasks.base import Task, TaskResponse


class QueryMultiplePersonas(Task):
    def __init__(self):
        super().__init__()
        self.query = ""
        with Path.open(ROOT_DIR / "data" / "personas.yaml") as f:
            self.personas: List[Dict[str, str]] = yaml.load(f, Loader=yaml.SafeLoader)

    def generate_prompt(self, query: str) -> str:
        self.query = query
        return ""

    def process_response(self, response: str) -> TaskResponse:
        next_requests = []
        for persona in self.personas:
            next_requests += [Request(persona["prompt"] + "\n" + self.query, "simple")]
        return TaskResponse(next_requests)
