import os

import dotenv
import pytest
from google.adk.agents import LlmAgent, Agent
from google.adk.tools.agent_tool import AgentTool

from proto_qa_agent.agent import proto_qa_coordinator, root_agent
from proto_qa_agent.sub_agents.proto_schema_validator import proto_schema_validator_agent
from proto_qa_agent.sub_agents.proto_test_generator import proto_test_generator_agent
from proto_qa_agent.sub_agents.proto_test_executor import proto_test_executor_agent
from proto_qa_agent.sub_agents.proto_qa_reporter import proto_qa_reporter_agent
from proto_qa_agent import prompt
from proto_qa_agent.sub_agents.proto_schema_validator import prompt as schema_prompt
from proto_qa_agent.sub_agents.proto_test_generator import prompt as gen_prompt
from proto_qa_agent.sub_agents.proto_test_executor import prompt as exec_prompt
from proto_qa_agent.sub_agents.proto_qa_reporter import prompt as reporter_prompt

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


class TestCoordinatorStructure:
    def test_root_agent_is_llm_agent(self):
        assert isinstance(root_agent, LlmAgent)

    def test_root_agent_is_coordinator(self):
        assert root_agent is proto_qa_coordinator

    def test_coordinator_name(self):
        assert root_agent.name == "proto_qa_coordinator"

    def test_coordinator_model(self):
        assert root_agent.model == "gemini-2.5-pro"

    def test_coordinator_output_key(self):
        assert root_agent.output_key == "qa_report_path"

    def test_coordinator_has_four_tools(self):
        assert len(root_agent.tools) == 4

    def test_coordinator_instruction_non_empty(self):
        assert len(root_agent.instruction) > 100

    def test_coordinator_prompt_has_gate_logic(self):
        assert "validation_results.json" in root_agent.instruction

    def test_coordinator_prompt_has_stop_instruction(self):
        instr = root_agent.instruction.lower()
        assert "stop" in instr or "halt" in instr or "do not proceed" in instr


class TestSubAgentStructure:
    def test_schema_validator_is_agent(self):
        assert isinstance(proto_schema_validator_agent, Agent)

    def test_schema_validator_name(self):
        assert proto_schema_validator_agent.name == "proto_schema_validator"

    def test_schema_validator_output_key(self):
        assert proto_schema_validator_agent.output_key == "validation_results"

    def test_test_generator_is_agent(self):
        assert isinstance(proto_test_generator_agent, Agent)

    def test_test_generator_name(self):
        assert proto_test_generator_agent.name == "proto_test_generator"

    def test_test_generator_output_key(self):
        assert proto_test_generator_agent.output_key == "test_cases"

    def test_test_executor_is_agent(self):
        assert isinstance(proto_test_executor_agent, Agent)

    def test_test_executor_name(self):
        assert proto_test_executor_agent.name == "proto_test_executor"

    def test_test_executor_output_key(self):
        assert proto_test_executor_agent.output_key == "test_results"

    def test_qa_reporter_is_agent(self):
        assert isinstance(proto_qa_reporter_agent, Agent)

    def test_qa_reporter_name(self):
        assert proto_qa_reporter_agent.name == "proto_qa_reporter"

    def test_qa_reporter_output_key(self):
        assert proto_qa_reporter_agent.output_key == "report_path"


class TestPromptContent:
    def test_all_prompts_non_empty(self):
        assert len(prompt.COORDINATOR_PROMPT) > 100
        assert len(schema_prompt.SCHEMA_VALIDATOR_PROMPT) > 100
        assert len(gen_prompt.TEST_GENERATOR_PROMPT) > 100
        assert len(exec_prompt.TEST_EXECUTOR_PROMPT) > 100
        assert len(reporter_prompt.QA_REPORTER_PROMPT) > 100

    def test_coordinator_prompt_has_gate(self):
        assert "validation_results.json" in prompt.COORDINATOR_PROMPT

    def test_schema_validator_prompt_has_output_path(self):
        assert "files/validation/validation_results.json" in schema_prompt.SCHEMA_VALIDATOR_PROMPT

    def test_test_generator_prompt_prohibits_fabrication(self):
        prompt_text = gen_prompt.TEST_GENERATOR_PROMPT.lower()
        assert "never" in prompt_text or "fabricat" in prompt_text

    def test_test_executor_prompt_has_proto_executor(self):
        assert "proto_executor" in exec_prompt.TEST_EXECUTOR_PROMPT

    def test_qa_reporter_prompt_has_validation_issues(self):
        assert "Validation Issues" in reporter_prompt.QA_REPORTER_PROMPT

    def test_qa_reporter_prompt_has_all_tests_passed(self):
        assert "All tests passed" in reporter_prompt.QA_REPORTER_PROMPT


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.getenv("GOOGLE_CLOUD_PROJECT"),
    reason="requires GCP project credentials"
)
async def test_happy_path_agent_responds():
    """Integration smoke test — requires GCP credentials."""
    import textwrap
    from google.adk.runners import InMemoryRunner
    from google.genai import types

    user_input = "Run QA on the proto files in specs/"
    app_name = "proto-qa-agent-adk"
    runner = InMemoryRunner(agent=root_agent, app_name=app_name)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    content = types.Content(parts=[types.Part(text=user_input)])
    response = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content and event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    assert len(response) > 0
