# Multi-Agent Research System (Vertex AI Edition)

A multi-agent research system that coordinates specialized subagents to research any topic and generate comprehensive PDF reports with data visualizations.

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

Then ask: "Research quantum computing developments in 2025"

## Authentication

This project uses **Vertex AI SDK** to access Claude through Google Cloud Platform using a monkey-patch approach.

### How Vertex AI Integration Works

The project uses a monkey-patch approach to integrate Vertex AI:

1. Before importing Claude Agent SDK, the code calls `patch_anthropic_for_vertex()`
2. This patches the Anthropic SDK to use `AnthropicVertex` client instead of standard `Anthropic` client
3. All subsequent API calls route through Vertex AI/GCP
4. Claude Agent SDK features (multi-agent, hooks, tools) work unchanged

See `research_agent/utils/vertex_patch.py` for implementation details.

## How It Works

1. **Lead Agent** breaks your request into 2-4 subtopics
2. Spawns **Researcher** subagents in parallel to search the web
3. Each Researcher saves findings to `files/research_notes/`
4. Spawns **Data Analyst** to extract metrics and generate charts in `files/charts/`
5. Spawns **Report Writer** to create final PDF report in `files/reports/`

## Agents

| Agent | Tools | Purpose |
|-------|-------|---------|
| **Lead Agent** | `Task` | Coordinates research, delegates to subagents |
| **Researcher** | `WebSearch`, `Write` | Gathers information from the web |
| **Data Analyst** | `Glob`, `Read`, `Bash`, `Write` | Extracts metrics, generates charts |
| **Report Writer** | `Skill`, `Write`, `Glob`, `Read`, `Bash` | Creates PDF reports with embedded visuals |

## Slash Commands

| Command | Description |
|---------|-------------|
| `/research <topic>` | Start focused research on any topic |
| `/competitive-analysis <company>` | Analyze companies or products |
| `/market-trends <industry>` | Research industry trends |
| `/fact-check <claim>` | Verify claims and statements |
| `/summarize` | Summarize all current research findings |

## Example Queries

- "Research quantum computing developments"
- "What are current trends in renewable energy?"
- `/competitive-analysis Tesla`
- `/market-trends artificial intelligence`

## Output Structure

```
files/
├── research_notes/     # Markdown files from researchers
├── data/               # Data summaries from analyst
├── charts/             # PNG visualizations
└── reports/            # Final PDF reports

logs/
└── session_YYYYMMDD_HHMMSS/
    ├── transcript.txt      # Human-readable conversation
    └── tool_calls.jsonl    # Structured tool usage log
```

## Subagent Tracking with Hooks

The system tracks all tool calls using SDK hooks.

### What Gets Tracked

- **Who**: Which agent (RESEARCHER-1, DATA-ANALYST-1, etc.)
- **What**: Tool name (WebSearch, Write, Bash, etc.)
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

The `parent_tool_use_id` links tool calls to their subagent:
- Lead Agent spawns a Researcher via `Task` tool → gets ID "task_123"
- All tool calls from that Researcher include `parent_tool_use_id = "task_123"`
- Hooks use this ID to identify which subagent made the call

### Log Output

**transcript.txt** - Human-readable:
```
[RESEARCHER-1] → WebSearch
    Input: query='quantum computing 2025'
[DATA-ANALYST-1] → Bash
    Input: python matplotlib chart generation
```

**tool_calls.jsonl** - Structured JSON:
```json
{"event":"tool_call_start","agent_id":"RESEARCHER-1","tool_name":"WebSearch",...}
{"event":"tool_call_complete","success":true,"output_size":15234}
```
