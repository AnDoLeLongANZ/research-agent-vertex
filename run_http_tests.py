import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List
import requests


def execute_http_test(test_case: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()

    result = {
        "test_id": test_case["test_id"],
        "test_type": test_case["test_type"],
        "endpoint_path": test_case["endpoint_path"],
        "expected_status": test_case["expected_status"],
        "actual_status": None,
        "passed": False,
        "latency_ms": None,
        "request_body": test_case.get("request_body"),
        "response_body": None,
        "error": None
    }

    try:
        method = test_case.get("method", "GET").upper()
        headers = test_case.get("headers", {})
        request_body = test_case.get("request_body")

        url = f"https://api.example.com{test_case['endpoint_path']}"

        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=request_body, headers=headers, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=request_body, headers=headers, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        elif method == "PATCH":
            response = requests.patch(url, json=request_body, headers=headers, timeout=10)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000

        result["actual_status"] = response.status_code
        result["latency_ms"] = round(latency_ms, 2)
        result["passed"] = response.status_code == test_case["expected_status"]

        try:
            result["response_body"] = response.json()
        except ValueError:
            result["response_body"] = response.text

    except requests.exceptions.Timeout:
        end_time = time.time()
        result["latency_ms"] = round((end_time - start_time) * 1000, 2)
        result["error"] = "Request timeout"

    except requests.exceptions.ConnectionError as e:
        end_time = time.time()
        result["latency_ms"] = round((end_time - start_time) * 1000, 2)
        result["error"] = f"Connection error: {str(e)}"

    except requests.exceptions.RequestException as e:
        end_time = time.time()
        result["latency_ms"] = round((end_time - start_time) * 1000, 2)
        result["error"] = f"Request error: {str(e)}"

    except Exception as e:
        end_time = time.time()
        result["latency_ms"] = round((end_time - start_time) * 1000, 2)
        result["error"] = f"Unexpected error: {str(e)}"

    return result


def main():
    test_cases_path = Path("/Users/doa4/Repositories/agentic-testing/research-agent-vertex/files/test_cases/test_cases.json")
    results_path = Path("/Users/doa4/Repositories/agentic-testing/research-agent-vertex/files/test_results/results.json")

    results_path.parent.mkdir(parents=True, exist_ok=True)

    with open(test_cases_path, 'r') as f:
        test_cases = json.load(f)

    print(f"Loaded {len(test_cases)} test cases")
    print("Executing tests concurrently...")

    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_test = {executor.submit(execute_http_test, test): test for test in test_cases}

        for future in as_completed(future_to_test):
            test = future_to_test[future]
            try:
                result = future.result()
                results.append(result)
                status = "PASS" if result["passed"] else "FAIL"
                print(f"  [{status}] {result['test_id']} - {result['actual_status'] or 'ERROR'} (expected: {result['expected_status']}) - {result['latency_ms']}ms")
            except Exception as e:
                print(f"  [ERROR] {test['test_id']} - Exception: {str(e)}")

    results_sorted = sorted(results, key=lambda x: x["test_id"])

    with open(results_path, 'w') as f:
        json.dump(results_sorted, f, indent=2)

    print(f"\nResults saved to: {results_path}")

    passed = sum(1 for r in results_sorted if r["passed"])
    total = len(results_sorted)
    print(f"\nSummary: {passed}/{total} tests passed")

    return results_sorted


if __name__ == "__main__":
    main()
