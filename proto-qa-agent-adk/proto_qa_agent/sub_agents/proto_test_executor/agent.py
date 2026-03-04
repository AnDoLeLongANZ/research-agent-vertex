import os

from google.adk import Agent

from proto_qa_agent.tools import read_file, run_python_snippet, write_json

from . import prompt

MODEL = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.5-pro")

proto_test_executor_agent = Agent(
    name="proto_test_executor",
    model=MODEL,
    description="Executes proto serialization round-trip tests and writes results to files/test_results/results.json.",
    instruction=prompt.TEST_EXECUTOR_PROMPT,
    output_key="test_results",
    tools=[read_file, write_json, run_python_snippet],
)
