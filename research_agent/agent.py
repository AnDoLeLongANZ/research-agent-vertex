"""Entry point for research agent using AgentDefinition for subagents.

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


async def chat():
    """Start interactive chat with the research agent."""

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
    researcher_prompt = load_prompt("researcher.txt")
    data_analyst_prompt = load_prompt("data_analyst.txt")
    report_writer_prompt = load_prompt("report_writer.txt")

    # Initialize subagent tracker with transcript writer and session directory
    tracker = SubagentTracker(transcript_writer=transcript, session_dir=session_dir)

    # Define specialized subagents
    agents = {
        "researcher": AgentDefinition(
            description=(
                "Use this agent when you need to gather research information on any topic. "
                "The researcher uses web search to find relevant information, articles, and sources "
                "from across the internet. Writes research findings to files/research_notes/ "
                "for later use by report writers. Ideal for complex research tasks "
                "that require deep searching and cross-referencing."
            ),
            tools=["WebSearch", "Write"],
            prompt=researcher_prompt,
            model=CLAUDE_MODEL
        ),
        "data-analyst": AgentDefinition(
            description=(
                "Use this agent AFTER researchers have completed their work to generate quantitative "
                "analysis and visualizations. The data-analyst reads research notes from files/research_notes/, "
                "extracts numerical data (percentages, rankings, trends, comparisons), and generates "
                "charts using Python/matplotlib via Bash. Saves charts to files/charts/ and writes "
                "a data summary to files/data/. Use this before the report-writer to add visual insights."
            ),
            tools=["Glob", "Read", "Bash", "Write"],
            prompt=data_analyst_prompt,
            model=CLAUDE_MODEL
        ),
        "report-writer": AgentDefinition(
            description=(
                "Use this agent when you need to create a formal research report document. "
                "The report-writer reads research findings from files/research_notes/, data analysis "
                "from files/data/, and charts from files/charts/, then synthesizes them into clear, "
                "concise, professionally formatted PDF reports in files/reports/ using reportlab. "
                "Ideal for creating structured documents with proper citations, data, and embedded visuals. "
                "Does NOT conduct web searches - only reads existing research notes and creates PDF reports."
            ),
            tools=["Skill", "Write", "Glob", "Read", "Bash"],
            prompt=report_writer_prompt,
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
    print("  Research Agent")
    print("=" * 50)
    print("\nResearch any topic and get a comprehensive PDF")
    print("report with data visualizations.")
    print("\nType 'exit' to quit.\n")

    try:
        async with ClaudeSDKClient(options=options) as client:
            while True:
                # Get input
                try:
                    user_input = input("\nYou: ").strip()
                except (EOFError, KeyboardInterrupt):
                    break

                if not user_input or user_input.lower() in ["exit", "quit", "q"]:
                    break

                # Write user input to transcript (file only, not console)
                transcript.write_to_file(f"\nYou: {user_input}\n")

                # Send to agent
                await client.query(prompt=user_input)

                transcript.write("\nAgent: ", end="")

                # Stream and process response
                async for msg in client.receive_response():
                    if type(msg).__name__ == 'AssistantMessage':
                        process_assistant_message(msg, tracker, transcript)

                transcript.write("\n")
    finally:
        transcript.write("\n\nGoodbye!\n")
        transcript.close()
        tracker.close()
        print(f"\nSession logs saved to: {session_dir}")
        print(f"  - Transcript: {transcript_file}")
        print(f"  - Tool calls: {session_dir / 'tool_calls.jsonl'}")


if __name__ == "__main__":
    asyncio.run(chat())
