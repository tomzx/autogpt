import os
from argparse import ArgumentParser

import structlog
from dask import delayed
from distributed import Client
from dotenv import load_dotenv

from autogpt.agents.agent import execute
from autogpt.configuration.configuration import Configuration
from autogpt.tasks import all_tasks_names

logger = structlog.get_logger(__name__)


if __name__ == "__main__":
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--prompt", type=str, help="The prompt to provide to the task")
    argument_parser.add_argument("--budget", type=float, help="Maximum budget to spend before terminating, in USD")
    argument_parser.add_argument("--task", type=str, default="simple", choices=all_tasks_names, help="Task to run")
    argument_parser.add_argument("--background", action="store_true", help="Run in background mode")

    args = argument_parser.parse_args()

    scheduler_url = Configuration.scheduler_url
    try:
        client = Client(scheduler_url, timeout=5)
    except OSError as e:
        print(f"Could not connect to scheduler: {e}")
        exit(1)

    response = delayed(execute)(args.prompt, args.task, args.budget, args.background).compute()

    client.close()
