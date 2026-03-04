import os

from google.adk import Agent

from proto_qa_agent.tools import list_proto_files, read_file, write_json

from . import prompt

MODEL = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.5-pro")

proto_test_generator_agent = Agent(
    name="proto_test_generator",
    model=MODEL,
    description="Generates positive and negative serialization test cases from proto definitions. Writes test cases to files/test_cases/test_cases.json.",
    instruction=prompt.TEST_GENERATOR_PROMPT,
    output_key="test_cases",
    tools=[list_proto_files, read_file, write_json],
)
