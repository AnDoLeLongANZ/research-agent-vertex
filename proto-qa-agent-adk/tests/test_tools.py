import json
import os
import pytest
from proto_qa_agent.tools import read_file, write_json, write_file, list_proto_files, run_python_snippet


class TestReadFile:
    def test_read_file_success(self, tmp_path):
        # Create a temp file and read it
        f = tmp_path / "test.txt"
        f.write_text("hello world")
        result = read_file(str(f))
        assert result == "hello world"

    def test_read_file_not_found(self):
        result = read_file("/nonexistent/path/file.txt")
        assert result.startswith("ERROR: File not found")
        assert "/nonexistent/path/file.txt" in result

    def test_read_file_does_not_raise(self):
        # Must return error string, not raise
        result = read_file("/nonexistent/path")
        assert isinstance(result, str)


class TestWriteJson:
    def test_write_json_creates_file(self, tmp_path):
        path = str(tmp_path / "output" / "test.json")
        result = write_json(path, json.dumps({"key": "value"}))
        assert result == f"Written: {path}"
        assert os.path.exists(path)
        with open(path) as f:
            data = json.load(f)
        assert data == {"key": "value"}

    def test_write_json_creates_parent_dirs(self, tmp_path):
        path = str(tmp_path / "a" / "b" / "c" / "test.json")
        write_json(path, json.dumps({}))
        assert os.path.exists(path)

    def test_write_json_returns_path(self, tmp_path):
        path = str(tmp_path / "test.json")
        result = write_json(path, json.dumps({"x": 1}))
        assert result == f"Written: {path}"

    def test_write_json_invalid_json(self, tmp_path):
        path = str(tmp_path / "test.json")
        result = write_json(path, "not valid json {{{")
        assert result.startswith("ERROR:")


class TestWriteFile:
    def test_write_file_creates_markdown(self, tmp_path):
        path = str(tmp_path / "reports" / "report.md")
        content = "# Report\n\n## Summary\n\nAll tests passed."
        result = write_file(path, content)
        assert result == f"Written: {path}"
        assert os.path.exists(path)
        with open(path) as f:
            assert f.read() == content

    def test_write_file_creates_parent_dirs(self, tmp_path):
        path = str(tmp_path / "a" / "b" / "file.txt")
        write_file(path, "content")
        assert os.path.exists(path)


class TestListProtoFiles:
    def test_list_proto_files_found(self, tmp_path):
        # Create .proto files
        (tmp_path / "a.proto").write_text("syntax = 'proto3';")
        (tmp_path / "b.proto").write_text("syntax = 'proto3';")
        result = list_proto_files(str(tmp_path))
        lines = [l for l in result.split("\n") if l]
        assert len(lines) == 2
        assert all(l.endswith(".proto") for l in lines)

    def test_list_proto_files_empty(self, tmp_path):
        result = list_proto_files(str(tmp_path))
        assert result == ""

    def test_list_proto_files_nonexistent_directory(self):
        result = list_proto_files("/nonexistent/dir")
        # Should return empty string (not error) — glob returns [] for missing dirs
        assert isinstance(result, str)

    def test_list_proto_files_ignores_non_proto(self, tmp_path):
        (tmp_path / "a.proto").write_text("syntax = 'proto3';")
        (tmp_path / "b.txt").write_text("text")
        result = list_proto_files(str(tmp_path))
        lines = [l for l in result.split("\n") if l]
        assert len(lines) == 1


class TestRunPythonSnippet:
    def test_run_python_snippet_success(self):
        result = run_python_snippet("print('hello')")
        assert "hello" in result

    def test_run_python_snippet_error(self):
        result = run_python_snippet("raise ValueError('test error')")
        assert "ERROR" in result

    def test_run_python_snippet_returns_string(self):
        result = run_python_snippet("x = 1 + 1; print(x)")
        assert isinstance(result, str)
