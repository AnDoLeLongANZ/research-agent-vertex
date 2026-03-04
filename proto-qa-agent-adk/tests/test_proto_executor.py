import json
import pytest
from proto_qa_agent.lib.proto_executor import get_message_class, run_test, run_all_tests


class TestDescriptorLoader:
    """Test suite for proto descriptor loading and message class retrieval."""

    @pytest.fixture
    def example_proto_path(self):
        """Return the path to the example.proto test fixture."""
        return "specs/example.proto"

    def test_get_message_class_success(self, example_proto_path):
        """Test successful retrieval of message class from proto file."""
        msg_class = get_message_class(example_proto_path, "Ping")
        assert msg_class is not None
        assert msg_class.DESCRIPTOR.name == "Ping"

    def test_get_message_class_nonexistent_message(self, example_proto_path):
        """Test that KeyError is raised when message name doesn't exist."""
        with pytest.raises(KeyError, match="Message .* not found"):
            get_message_class(example_proto_path, "NonExistentMessage")

    def test_get_message_class_idempotent(self, example_proto_path):
        """Test that loading the same proto file twice doesn't raise TypeError."""
        msg_class1 = get_message_class(example_proto_path, "Ping")
        msg_class2 = get_message_class(example_proto_path, "Ping")
        assert msg_class1 is msg_class2


class TestSerializationRoundTrip:
    """Test suite for serialization round-trip test execution."""

    def test_run_test_positive_case_success(self):
        """Test a positive case with valid input data that should succeed."""
        test_case = {
            "test_id": "tc_001",
            "test_type": "positive",
            "proto_file": "specs/example.proto",
            "message_name": "Ping",
            "input_data": {"id": "test123"},
            "expected_outcome": "success",
        }

        result = run_test(test_case)

        assert result["test_id"] == "tc_001"
        assert result["test_type"] == "positive"
        assert result["proto_file"] == "specs/example.proto"
        assert result["message_name"] == "Ping"
        assert result["passed"] is True
        assert result["actual_outcome"] == "success"
        assert result["error"] is None
        assert result["duration_ms"] >= 0

    def test_run_test_positive_case_with_empty_data(self):
        """Test a positive case with empty input data."""
        test_case = {
            "test_id": "tc_002",
            "test_type": "positive",
            "proto_file": "specs/example.proto",
            "message_name": "Ping",
            "input_data": {},
            "expected_outcome": "success",
        }

        result = run_test(test_case)

        assert result["passed"] is True
        assert result["actual_outcome"] == "success"

    def test_run_test_negative_case_nonexistent_message(self):
        """Test a negative case where the message doesn't exist."""
        test_case = {
            "test_id": "tc_003",
            "test_type": "negative",
            "proto_file": "specs/example.proto",
            "message_name": "NonExistent",
            "input_data": {},
            "expected_outcome": "error:KeyError",
        }

        result = run_test(test_case)

        assert result["passed"] is True
        assert result["actual_outcome"].startswith("error:")
        assert result["error"] is not None

    def test_run_test_negative_case_type_mismatch(self):
        """Test a negative case with invalid field type should fail as negative test."""
        test_case = {
            "test_id": "tc_004",
            "test_type": "negative",
            "proto_file": "specs/example.proto",
            "message_name": "Ping",
            "input_data": {"id": 12345},
            "expected_outcome": "error:TypeError",
        }

        result = run_test(test_case)

        assert result["test_id"] == "tc_004"
        assert result["actual_outcome"].startswith("error:")
        assert result["error"] is not None


class TestBatchRunner:
    """Test suite for batch test execution and JSON I/O."""

    @pytest.fixture
    def sample_test_cases(self):
        """Sample test cases for batch execution."""
        return [
            {
                "test_id": "tc_001",
                "test_type": "positive",
                "proto_file": "specs/example.proto",
                "message_name": "Ping",
                "input_data": {"id": "test1"},
                "expected_outcome": "success",
            },
            {
                "test_id": "tc_002",
                "test_type": "positive",
                "proto_file": "specs/example.proto",
                "message_name": "Ping",
                "input_data": {},
                "expected_outcome": "success",
            },
            {
                "test_id": "tc_003",
                "test_type": "negative",
                "proto_file": "specs/example.proto",
                "message_name": "NonExistent",
                "input_data": {},
                "expected_outcome": "error:KeyError",
            },
        ]

    def test_run_all_tests_no_output_file(self, sample_test_cases):
        """Test batch execution without writing to output file."""
        results = run_all_tests(sample_test_cases)

        assert len(results) == 3
        assert all(r["test_id"] in ["tc_001", "tc_002", "tc_003"] for r in results)
        assert results[0]["test_id"] == "tc_001"
        assert results[1]["test_id"] == "tc_002"
        assert results[2]["test_id"] == "tc_003"

    def test_run_all_tests_with_output_file(self, sample_test_cases, tmp_path):
        """Test batch execution with JSON output file."""
        output_file = tmp_path / "results.json"
        results = run_all_tests(sample_test_cases, output_path=str(output_file))

        assert output_file.exists()
        with open(output_file) as f:
            saved_results = json.load(f)

        assert len(saved_results) == 3
        assert saved_results == results

    def test_run_all_tests_sorted_by_id(self):
        """Test that results are sorted by test_id."""
        test_cases = [
            {
                "test_id": "tc_003",
                "test_type": "positive",
                "proto_file": "specs/example.proto",
                "message_name": "Ping",
                "input_data": {},
                "expected_outcome": "success",
            },
            {
                "test_id": "tc_001",
                "test_type": "positive",
                "proto_file": "specs/example.proto",
                "message_name": "Ping",
                "input_data": {"id": "test"},
                "expected_outcome": "success",
            },
        ]

        results = run_all_tests(test_cases)

        assert results[0]["test_id"] == "tc_001"
        assert results[1]["test_id"] == "tc_003"
