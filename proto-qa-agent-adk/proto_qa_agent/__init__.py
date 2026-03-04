"""Proto QA Agent: validates proto schemas, generates and executes serialization tests, and produces QA reports."""

import os

from dotenv import load_dotenv

load_dotenv(override=True)

os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
