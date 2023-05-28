from argparse import ArgumentParser
from uuid import uuid4

import requests
import structlog
import uvicorn
from fastapi import FastAPI

from autogpt.configuration.configuration import Configuration
from autogpt.server.routes import agent, openai, registry

logger = structlog.get_logger(__name__)

app = FastAPI()

app.include_router(agent.router)
app.include_router(registry.agent.router, prefix="/registry")
app.include_router(openai.router)

if __name__ == "__main__":
    argument_parser = ArgumentParser()

    argument_parser.add_argument("--host", default="0.0.0.0", type=str, help="Host to listen on")
    argument_parser.add_argument("--port", default=8000, type=int, help="Port to listen on")
    argument_parser.add_argument(
        "--name", default="main", type=str, help="Name of the agent (main reserved for controller)"
    )

    args = argument_parser.parse_args()

    if Configuration.agent_registry_url and args.name != "main":
        logger.debug("Registering to the agent registry", agent_registry=Configuration.agent_registry_url)
        requests.post(
            f"{Configuration.agent_registry_url}/registry/agents",
            json={
                "name": str(uuid4()),
                "url": f"http://{args.host}:{args.port}",
            },
        )

    uvicorn.run(app, host=args.host, port=args.port)

    # TODO(tom@tomrochette.com): Unregister from the agent registry on stop/crash
