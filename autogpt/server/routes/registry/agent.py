from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/agents")
agents = {}


class Agent(BaseModel):
    name: str
    url: str
    last_seen: Optional[datetime] = None


@router.get("/")
def index() -> Dict[str, Any]:
    return agents


@router.post("/")
def create(agent: Agent) -> Agent:
    if agent.name in agents:
        raise HTTPException(409, "Agent already exists")
    agents[agent.name] = agent
    agent.last_seen = datetime.now()
    return agent


@router.get("/{agent_id}")
def read(agent_id: str) -> Optional[Dict[str, Any]]:
    agent = agents.get(agent_id)

    if agent is None:
        raise HTTPException(404, "Agent does not exist")

    return agent


@router.put("/{agent_id}")
def update(agent_id: str, agent: Agent) -> Agent:
    agents[agent_id] = agent
    return agent


@router.delete("/{agent_id}")
def delete(agent_id: str) -> bool:
    deleted = agents.pop(agent_id, None) is not None
    return deleted
