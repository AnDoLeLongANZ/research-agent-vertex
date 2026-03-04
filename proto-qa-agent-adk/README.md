# Proto QA Agent (Google ADK)

An agentic Proto QA pipeline built on Google ADK. Validates proto3 schema files, generates serialization test cases, executes round-trip tests, and produces a structured Markdown QA report.

## Architecture

Four specialized sub-agents orchestrated by a root `LlmAgent` coordinator:

1. **proto_schema_validator** — validates syntax, field types, naming conventions
2. **proto_test_generator** — generates positive and negative test cases per proto message
3. **proto_test_executor** — executes serialization round-trip tests
4. **proto_qa_reporter** — writes a structured Markdown QA report

Sub-agents communicate via JSON files in `files/`. The coordinator halts if validation fails.

## Prerequisites

- Python 3.10–3.12
- [uv](https://docs.astral.sh/uv/) package manager
- `protoc` (Protocol Buffer compiler): `brew install protobuf` or equivalent
- GCP project with Vertex AI API enabled
- Application Default Credentials configured: `gcloud auth application-default login`

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Copy and configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and set GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION

   export GOOGLE_CLOUD_PROJECT=<YOUR_PROJECT_ID>
   ```

3. Add your `.proto` files to `specs/`:
   ```bash
   cp your_api.proto specs/
   ```

## Run

```bash
# CLI
adk run proto_qa_agent

# Web UI
adk web
```

## Output

After a successful run, outputs are written to:
- `files/validation/validation_results.json` — schema validation results
- `files/test_cases/test_cases.json` — generated test cases
- `files/test_results/results.json` — execution results
- `files/reports/qa_report_YYYYMMDD.md` — final QA report

## Run Tests

```bash
# Unit tests (no GCP required)
uv run pytest tests/ -v --ignore=tests/test_integration.py

# Integration tests (requires GCP)
uv run pytest tests/test_integration.py -v

# Evaluation (requires GCP)
uv run pytest eval/ -v
```

## Lint and Type Check

```bash
uv run ruff check .
uv run ruff format .
uv run mypy proto_qa_agent/
```

## Deploy to Vertex AI Agent Engine

```bash
uv sync --group deployment
uv run deployment/deploy.py --create

# List deployed agents
uv run deployment/deploy.py --list

# Delete a deployed agent
uv run deployment/deploy.py --delete --resource_id=<RESOURCE_ID>
```

Note: `protoc` must be available on the Agent Engine instance. Include it in your deployment environment setup.

## Proto File Format

Files in `specs/` must use `proto3` syntax:

```proto
syntax = "proto3";

message YourMessage {
  string field_name = 1;
  int32 count = 2;
}
```

Supported field types: `string`, `int32`, `int64`, `bool`, `bytes`, `double`, `float`, `repeated <type>`.
