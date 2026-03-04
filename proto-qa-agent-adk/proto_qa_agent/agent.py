import os

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.proto_schema_validator import proto_schema_validator_agent
from .sub_agents.proto_test_generator import proto_test_generator_agent
from .sub_agents.proto_test_executor import proto_test_executor_agent
from .sub_agents.proto_qa_reporter import proto_qa_reporter_agent

MODEL = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.5-pro")

proto_qa_coordinator = LlmAgent(
    name="proto_qa_coordinator",
    model=MODEL,
    description=(
        "Orchestrates a 4-stage proto QA pipeline: validates proto schemas, "
        "generates test cases, executes serialization tests, and produces a Markdown QA report."
    ),
    instruction=prompt.COORDINATOR_PROMPT,
    output_key="qa_report_path",
    tools=[
        AgentTool(agent=proto_schema_validator_agent),
        AgentTool(agent=proto_test_generator_agent),
        AgentTool(agent=proto_test_executor_agent),
        AgentTool(agent=proto_qa_reporter_agent),
    ],
)

root_agent = proto_qa_coordinator
