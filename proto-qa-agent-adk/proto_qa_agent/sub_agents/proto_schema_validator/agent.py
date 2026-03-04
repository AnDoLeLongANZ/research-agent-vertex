import os

from google.adk import Agent

from proto_qa_agent.tools import list_proto_files, read_file, write_json

from . import prompt

MODEL = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.5-pro")

proto_schema_validator_agent = Agent(
    name="proto_schema_validator",
    model=MODEL,
    description="Validates proto3 schema files for syntax, field types, and naming conventions. Writes results to files/validation/validation_results.json.",
    instruction=prompt.SCHEMA_VALIDATOR_PROMPT,
    output_key="validation_results",
    tools=[list_proto_files, read_file, write_json],
)
