import glob as glob_module
import json
import os
import subprocess
import sys

from google.adk.tools import tool


@tool
def read_file(path: str) -> str:
    """Read the contents of a text file at the given path. Returns file contents or an error string."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: File not found: {path}"
    except Exception as e:
        return f"ERROR: {e}"


@tool
def write_json(path: str, content: str) -> str:
    """Write a JSON string to a file at the given path, creating parent directories as needed. Returns confirmation or error string."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        data = json.loads(content)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return f"Written: {path}"
    except json.JSONDecodeError as e:
        return f"ERROR: Invalid JSON — {e}"
    except Exception as e:
        return f"ERROR: {e}"


@tool
def write_file(path: str, content: str) -> str:
    """Write raw string content to a file at the given path, creating parent directories as needed. Returns confirmation or error string."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Written: {path}"
    except Exception as e:
        return f"ERROR: {e}"


@tool
def list_proto_files(directory: str) -> str:
    """List all .proto files in the given directory. Returns newline-delimited file paths, or empty string if none found."""
    try:
        files = glob_module.glob(f"{directory}/*.proto")
        return "\n".join(sorted(files)) if files else ""
    except Exception as e:
        return f"ERROR: {e}"


@tool
def run_python_snippet(code: str) -> str:
    """Execute a Python code snippet via subprocess and return stdout. Returns stderr string on error."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            return f"ERROR: {result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "ERROR: Timeout — snippet took longer than 120 seconds"
    except Exception as e:
        return f"ERROR: {e}"
