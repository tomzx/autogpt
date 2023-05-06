import os
from argparse import ArgumentParser

import structlog
from dask import delayed
from distributed import Client
from dotenv import load_dotenv

from autogpt.agents.agent import execute

logger = structlog.get_logger(__name__)


if __name__ == "__main__":
    argument_parser = ArgumentParser()
    argument_parser.add_argument("prompt")
    argument_parser.add_argument("--budget", type=float)

    args = argument_parser.parse_args()

    load_dotenv()

    scheduler_url = os.environ.get("SCHEDULER_URL")
    try:
        client = Client(scheduler_url, timeout=5)
    except OSError as e:
        print(f"Could not connect to scheduler: {e}")
        exit(1)

    response = delayed(execute)(args.prompt, args.budget).compute()

    # response = client.submit(execute, args.prompt, args.budget)

    # Wait for the request to have been processed before exiting
    # response.result()

    client.close()
