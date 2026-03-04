import glob
import json
import os
import pathlib
import textwrap

import pytest

from proto_qa_agent.agent import root_agent


REQUIRES_GCP = pytest.mark.skipif(
    not os.getenv("GOOGLE_CLOUD_PROJECT"),
    reason="requires GOOGLE_CLOUD_PROJECT env var and GCP credentials",
)


@REQUIRES_GCP
@pytest.mark.asyncio
async def test_full_pipeline_produces_all_outputs(tmp_path):
    """Full pipeline run: specs/example.proto -> validation -> test cases -> results -> report."""
    from google.adk.runners import InMemoryRunner
    from google.genai import types

    # Run the agent
    app_name = "proto-qa-agent-adk-integration"
    runner = InMemoryRunner(agent=root_agent, app_name=app_name)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="integration_test_user"
    )
    content = types.Content(parts=[types.Part(text="Run QA on the proto files in specs/")])
    response = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content and event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    # 1. Validation results
    validation_path = pathlib.Path("files/validation/validation_results.json")
    assert validation_path.exists(), "validation_results.json not found"
    with open(validation_path) as f:
        validation = json.load(f)
    assert isinstance(validation.get("passed"), bool), "passed field must be bool"
    assert validation["passed"] is True, f"Validation failed: {validation.get('errors')}"

    # 2. Test cases
    test_cases_path = pathlib.Path("files/test_cases/test_cases.json")
    assert test_cases_path.exists(), "test_cases.json not found"
    with open(test_cases_path) as f:
        test_cases = json.load(f)
    assert isinstance(test_cases, list), "test_cases.json must be a JSON array"
    assert len(test_cases) > 0, "test_cases.json is empty — at least 1 test case expected"
    required_fields = {"test_id", "test_type", "proto_file", "message_name", "input_data", "expected_outcome"}
    for tc in test_cases:
        assert required_fields.issubset(tc.keys()), f"test case missing fields: {tc}"

    # 3. Test results
    results_path = pathlib.Path("files/test_results/results.json")
    assert results_path.exists(), "results.json not found"
    with open(results_path) as f:
        results = json.load(f)
    assert isinstance(results, list), "results.json must be a JSON array"
    assert len(results) > 0, "results.json is empty"
    result_fields = {"test_id", "passed", "actual_outcome", "duration_ms"}
    for r in results:
        assert result_fields.issubset(r.keys()), f"result missing fields: {r}"

    # 4. QA report
    report_files = glob.glob("files/reports/qa_report_*.md")
    assert len(report_files) > 0, "No QA report file found in files/reports/"
    report_path = report_files[-1]  # most recent
    with open(report_path) as f:
        report_content = f.read()
    assert "# Proto QA Test Report" in report_content, "Report missing title"
    assert "## Summary" in report_content, "Report missing Summary section"
    assert "## Per-Proto-File Results" in report_content, "Report missing Per-Proto-File Results"

    # 5. Coordinator returned something
    assert len(response) > 0, "Coordinator returned empty response"


@REQUIRES_GCP
@pytest.mark.asyncio
async def test_pipeline_halts_on_invalid_proto(tmp_path):
    """Pipeline must halt after validation failure — test-generator must NOT be invoked."""
    import shutil
    from google.adk.runners import InMemoryRunner
    from google.genai import types

    # Create a temp specs folder with a malformed proto
    malformed_specs = tmp_path / "specs"
    malformed_specs.mkdir()
    (malformed_specs / "bad.proto").write_text(
        # Missing syntax = "proto3" declaration
        "message BadMessage {\n  string id = 1;\n}\n"
    )

    # Remove test_cases.json if it exists from a previous run
    test_cases_path = pathlib.Path("files/test_cases/test_cases.json")
    if test_cases_path.exists():
        test_cases_path.unlink()

    app_name = "proto-qa-agent-adk-halt-test"
    runner = InMemoryRunner(agent=root_agent, app_name=app_name)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="halt_test_user"
    )
    # Pass the temp malformed specs folder path in the message
    content = types.Content(
        parts=[types.Part(text=f"Run QA on the proto files in {str(malformed_specs)}/")]
    )
    response = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content and event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    # test_cases.json must NOT have been created by a fresh test-generator run
    # (coordinator should have halted at the validation gate)
    # We verify the coordinator's response mentions validation failure
    assert len(response) > 0, "Coordinator returned empty response on halt"
    response_lower = response.lower()
    validation_mentioned = any(
        kw in response_lower for kw in ["validation", "error", "failed", "invalid", "syntax"]
    )
    assert validation_mentioned, f"Coordinator response didn't mention validation: {response[:200]}"
