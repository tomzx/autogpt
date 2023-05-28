from typing import Any, Dict

from fastapi import APIRouter

from autogpt.server.agent import agent
from autogpt.tasks import all_tasks_names

router = APIRouter(prefix="/agents")


@router.get("/tasks")
def tasks():
    return all_tasks_names


@router.post("/query")
def query(request: str, task: str) -> Dict[str, Any]:
    # TODO(tom@tomrochette.com): Authenticate and authorize prior to querying
    response = agent.execute(request, task)
    return {
        "response": response.response,
        "cost": response.cost,
    }


@router.get("/ping")
def ping() -> str:
    return "OK"
