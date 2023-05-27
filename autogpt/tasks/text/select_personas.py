from pathlib import Path
from typing import Dict, List

import yaml

from autogpt import ROOT_DIR
from autogpt.middlewares.next_requests import NextRequests
from autogpt.tasks.base import Task, TaskResponse

with Path.open(ROOT_DIR / "data" / "personas.yaml") as f:
    personas: List[Dict[str, str]] = yaml.load(f, Loader=yaml.SafeLoader)


class SelectPersonas(Task):
    name = "select-personas"

    def generate_prompt(self, query: str) -> str:
        personas_str = "\n".join([f"- {persona['name']}" for persona in personas])

        return f"""
Select personas that would best answer the following query: {query}
Available personas:
{personas_str}
Reply with only the names of the personas, separating them with a comma.
"""

    def process_response(self, response: str) -> TaskResponse:
        next_requests = NextRequests()
        return TaskResponse(next_requests)
