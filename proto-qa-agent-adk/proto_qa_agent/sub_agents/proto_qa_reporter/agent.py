import os

from google.adk import Agent

from proto_qa_agent.tools import read_file, write_file

from . import prompt

MODEL = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.5-pro")

proto_qa_reporter_agent = Agent(
    name="proto_qa_reporter",
    model=MODEL,
    description="Generates a structured Markdown QA report from test results and validation output. Writes report to files/reports/qa_report_YYYYMMDD.md.",
    instruction=prompt.QA_REPORTER_PROMPT,
    output_key="report_path",
    tools=[read_file, write_file],
)
