# QA Testing Agent (Vertex AI Edition)

A single-shot QA testing pipeline that reads an OpenAPI specification, generates test cases, executes them against the API endpoints, and produces a Markdown report.

**Key Difference**: This version uses Vertex AI SDK for authentication to access Claude via Google Cloud Platform, while maintaining the Claude Agent SDK for agentic framework features (tool use, MCP servers, conversation management).

## Quick Start

```bash
# Install dependencies
uv sync

# Authenticate with Google Cloud (Application Default Credentials)
gcloud auth login --update-adc

# Configure Vertex AI via environment variables
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_LOCATION="global"

# Or create a .env file with these variables

# Run the agent
uv run python research_agent/agent.py
```

## Pipeline Overview

The agent runs a single-shot pipeline in the following order:

1. Reads API specs to discover all API endpoints
2. Generates test cases covering each endpoint (happy path, error cases, edge cases)
3. Executes each test case against the target API server
4. Produces a Markdown report summarising pass/fail status and latency metrics

No interactive prompts are required. Running the command above starts and completes the full pipeline automatically.

## Authentication

This project uses **Vertex AI SDK** to access Claude through Google Cloud Platform using a monkey-patch approach.

### How Vertex AI Integration Works

The project uses a monkey-patch approach to integrate Vertex AI:

1. Before importing Claude Agent SDK, the code calls `patch_anthropic_for_vertex()`
2. This patches the Anthropic SDK to use `AnthropicVertex` client instead of standard `Anthropic` client
3. All subsequent API calls route through Vertex AI/GCP
4. Claude Agent SDK features (multi-agent, hooks, tools) work unchanged

See `research_agent/utils/vertex_patch.py` for implementation details.

## Subagent Tracking with Hooks

The system tracks all tool calls using SDK hooks.

### What Gets Tracked

- **Who**: Which agent made the call
- **What**: Tool name (Write, Read, Bash, etc.)
- **When**: Timestamp
- **Input/Output**: Parameters and results

### How It Works

Hooks intercept every tool call before and after execution:

```python
hooks = Hooks(
    pre_tool_use=[tracker.pre_tool_use_hook],
    post_tool_use=[tracker.post_tool_use_hook]
)
```

### Log Output

**transcript.txt** - Human-readable session log

**tool_calls.jsonl** - Structured JSON log of every tool call with event type, agent id, tool name, and timestamps
