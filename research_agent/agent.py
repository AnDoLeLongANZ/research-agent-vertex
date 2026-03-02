"""Entry point for QA testing agent using AgentDefinition for subagents.

  agent.py: model="haiku"
      ↓
  Claude Agent SDK: accepts shorthand
      ↓
  AnthropicVertex: constructs endpoint URL
      ↓
  Vertex AI API: /models/haiku:rawPredict
      ↓
  Resolves to: claude-3-5-haiku-20241022 or claude-haiku-4-5

"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Read and validate model selection
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "haiku").lower()
ALLOWED_MODELS = ["haiku", "sonnet", "opus"]

if CLAUDE_MODEL not in ALLOWED_MODELS:
    print(f"Warning: Invalid CLAUDE_MODEL '{CLAUDE_MODEL}'. Using default 'haiku'.")
    print(f"Allowed values: {', '.join(ALLOWED_MODELS)}")
    CLAUDE_MODEL = "haiku"

# Patch Anthropic SDK to use Vertex AI BEFORE importing claude_agent_sdk
from research_agent.utils.vertex_patch import patch_anthropic_for_vertex
from research_agent.utils.vertex_auth import verify_vertex_auth

patch_anthropic_for_vertex()

# Now import claude_agent_sdk (which will use our patched Anthropic client)
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition, HookMatcher

from research_agent.utils.subagent_tracker import SubagentTracker
from research_agent.utils.transcript import setup_session, TranscriptWriter
from research_agent.utils.message_handler import process_assistant_message

# Paths to prompt files
PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(filename: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = PROMPTS_DIR / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


async def run():
    """Run the QA testing pipeline in single-shot mode."""

    # Verify Vertex AI authentication first, before creating any files
    auth_ok, auth_message = verify_vertex_auth()
    if not auth_ok:
        print(f"\nError: {auth_message}")
        print("\nRequired environment variables:")
        print("  - GOOGLE_CLOUD_PROJECT: Your Google Cloud project ID")
        print("  - GOOGLE_CLOUD_LOCATION: GCP region (default: us-east5)")
        print("\nAuthentication:")
        print("  Run: gcloud auth login --update-adc")
        print("\nSet these in a .env file or export them in your shell.\n")
        return

    print(f"\nAuthentication: {auth_message}")
    print(f"Model: {CLAUDE_MODEL}\n")

    # Vertex AI client is already patched globally
    # Setup session directory and transcript
    transcript_file, session_dir = setup_session()

    # Create transcript writer
    transcript = TranscriptWriter(transcript_file)

    # Load prompts
    lead_agent_prompt = load_prompt("lead_agent.txt")
    test_generator_prompt = load_prompt("test_generator.txt")
    test_executor_prompt = load_prompt("test_executor.txt")
    qa_report_writer_prompt = load_prompt("qa_report_writer.txt")

    # Initialize subagent tracker with transcript writer and session directory
    tracker = SubagentTracker(transcript_writer=transcript, session_dir=session_dir)

    # Define specialized subagents
    agents = {
        "test-generator": AgentDefinition(
            description=(
                "Use this agent to generate QA test cases from an OpenAPI specification. "
                "The test-generator reads the spec at docs/specs/mock.openapi.json using Glob and Read, "
                "then produces positive and negative test cases for every endpoint. "
                "Writes structured test cases to files/test_cases/test_cases.json. "
                "Does NOT perform web searches — only reads the spec and writes test case files."
            ),
            tools=["Glob", "Read", "Bash", "Write"],
            prompt=test_generator_prompt,
            model=CLAUDE_MODEL
        ),
        "test-executor": AgentDefinition(
            description=(
                "Use this agent AFTER test-generator has completed to execute HTTP requests against the API. "
                "The test-executor reads test cases from files/test_cases/test_cases.json, "
                "sends concurrent HTTP requests via Python httpx with ThreadPoolExecutor, "
                "and writes structured results to files/test_results/results.json. "
                "Results include test_id, passed, actual_status, latency_ms, and error fields."
            ),
            tools=["Glob", "Read", "Bash", "Write"],
            prompt=test_executor_prompt,
            model=CLAUDE_MODEL
        ),
        "qa-report-writer": AgentDefinition(
            description=(
                "Use this agent AFTER test-executor has completed to generate a Markdown QA report. "
                "The qa-report-writer reads results from files/test_results/results.json, "
                "computes summary statistics and latency metrics, then writes a structured Markdown report "
                "to files/reports/qa_report_YYYYMMDD.md. "
                "Does NOT perform web searches — only reads results and writes the Markdown report."
            ),
            tools=["Glob", "Read", "Bash", "Write"],
            prompt=qa_report_writer_prompt,
            model=CLAUDE_MODEL
        )
    }

    # Set up hooks for tracking
    hooks = {
        'PreToolUse': [
            HookMatcher(
                matcher=None,  # Match all tools
                hooks=[tracker.pre_tool_use_hook]
            )
        ],
        'PostToolUse': [
            HookMatcher(
                matcher=None,  # Match all tools
                hooks=[tracker.post_tool_use_hook]
            )
        ]
    }

    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],  # Load skills from project .claude directory
        system_prompt=lead_agent_prompt,
        allowed_tools=["Task"],
        agents=agents,
        hooks=hooks,
        model=CLAUDE_MODEL
    )

    print("\n" + "=" * 50)
    print("  QA Testing Agent")
    print("=" * 50)
    print("\nRunning QA testing pipeline on docs/specs/mock.openapi.json")
    print()

    try:
        async with ClaudeSDKClient(options=options) as client:
            prompt = "Run QA testing pipeline on docs/specs/mock.openapi.json"
            transcript.write_to_file(f"\nPrompt: {prompt}\n")

            await client.query(prompt=prompt)

            transcript.write("\nAgent: ", end="")

            async for msg in client.receive_response():
                if type(msg).__name__ == 'AssistantMessage':
                    process_assistant_message(msg, tracker, transcript)

            transcript.write("\n")
    finally:
        transcript.write("\n\nDone.\n")
        transcript.close()
        tracker.close()
        print(f"\nSession logs saved to: {session_dir}")
        print(f"  - Transcript: {transcript_file}")
        print(f"  - Tool calls: {session_dir / 'tool_calls.jsonl'}")


if __name__ == "__main__":
    asyncio.run(run())
