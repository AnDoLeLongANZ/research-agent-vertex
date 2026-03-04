"""Basic evaluation for Proto QA Agent."""

import pathlib

import dotenv
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


@pytest.mark.asyncio
async def test_all():
    """Test the agent on eval data set. Requires GCP credentials."""
    await AgentEvaluator.evaluate(
        "proto_qa_agent",
        str(pathlib.Path(__file__).parent / "data"),
        num_runs=3,
    )
