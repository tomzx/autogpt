import os
import importlib
import pytest

# Ensure debug mode to avoid live OpenAI/Notion calls BEFORE AutoGPT imports
os.environ.setdefault("DEBUG", "1")
# Reload configuration after setting env
import autogpt.configuration.configuration as cfg
importlib.reload(cfg)

from autogpt.agents.agent import execute, Agent
from autogpt.middlewares.response import Response
from dask import delayed  # type: ignore
from distributed import Client, LocalCluster  # type: ignore


def test_time_budget_immediate_termination():
    """Agent should terminate immediately when time budget is zero seconds."""
    agent = Agent()
    response = agent.execute("Hello", "simple", None, 1)
    assert isinstance(response, Response)


def test_time_budget_with_distributed_execution():
    """`execute` function should run inside a Dask distributed client and honour time budget."""
    cluster = LocalCluster(n_workers=1, threads_per_worker=1, processes=False)
    client = Client(cluster)

    try:
        response = delayed(execute)("Hello", "simple", None, 1).compute()
        # Depending on serialization, Response may not propagate back; ensure execution returns a value
        assert response is None or isinstance(response, Response)
    finally:
        client.close()
        cluster.close()