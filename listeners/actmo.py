import builtins
import json
import os
import requests
import re
from datetime import datetime
from seleniumfw.listener_manager import (
    BeforeTestSuite,
    AfterTestSuite,
    BeforeTestCase,
    AfterTestCase,
)
from seleniumfw.config import Config

def get_date_parts_as_strings(datetime_str):
    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return {
        "date": dt.strftime("%d"),
        "month": dt.strftime("%B"),
        "year": dt.strftime("%Y"),
        "time": dt.strftime("%H:%M:%S")
    }


def to_readable_name(raw_path: str) -> str:
    """Convert a raw test case file path into a human-readable, capitalized name."""
    base = os.path.splitext(os.path.basename(raw_path))[0]
    base = base.replace("-", " ").replace("_", " ")
    base = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", base)
    base = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", base)
    return base.strip().title()


def extract_path_segment(testcase_path: str, index: int, humanize=True) -> str:
    """
    Extract folder part from a test case path, ignoring filename.
    """
    # Normalize and split
    parts = testcase_path.replace("\\", "/").split("/")

    # Remove file name if last part is a .py file
    if parts and parts[-1].endswith(".py"):
        parts = parts[:-1]

    if index >= len(parts):
        return ""

    value = parts[index]

    if humanize:
        value = re.sub(r'[^a-zA-Z_\s]', '', value)
        value = value.replace("_", " ").strip().title()

    return value

@BeforeTestSuite
def before_suite(suite_path):
    actmo_config = {
        "is_send_actmo": False,
        "actmo_url": "http://localhost:5001",
        "function_name": "PGD",
        "project_name": "Pegadaian Digital",
        "feature_index": 1,
        "subfeature_index": 2,
        "run_type": "local",
        "regression_name": "",
    }

    actmo_file_path = os.path.join(os.getcwd(), "settings", "actmo.properties")

    # Check if file already exists
    if not os.path.exists(actmo_file_path):
        os.makedirs(os.path.dirname(actmo_file_path), exist_ok=True)  # Ensure directory exists

        with open(actmo_file_path, "w", encoding="utf-8") as file:
            file.write("# Actmo configuration\n\n")
            for key, value in actmo_config.items():
                file.write(f"{key} = {str(value)}\n")

        print(f"actmo.properties created at {actmo_file_path}")
    else:
        print(f"actmo.properties already exists at {actmo_file_path}, skipping creation.")

@BeforeTestCase
def before_case(case, data=None):
    pass

@AfterTestCase
def after_case(case, data=None):
    pass

@AfterTestSuite
def after_suite(suite_path):
    config = Config()
    is_send_actmo = config.get('is_send_actmo', "False")
    print("is_send_actmo", is_send_actmo)
    if is_send_actmo.lower() == "false":
        print("No report send to actmo")
        return
    print("Sending to actmo...")
    # get report directory
    report = builtins._active_report
    report_dir = report.run_dir
    result_path = os.path.join(report_dir, "result.json")
    actmo_request = []
    id_test = os.path.basename(report_dir)
    # Extract report path
    report_path = report_dir.replace("\\", "/")

    if os.path.exists(result_path):
        with open(result_path, 'r', encoding='utf-8') as f:
            result_data = json.load(f)
            start_time = get_date_parts_as_strings(result_data['start_time'])
            end_time = get_date_parts_as_strings(result_data['end_time'])
            # Extract test suite
            testsuite_path = result_data['testsuite_id'].replace("\\", "/")
            base_filename = os.path.splitext(os.path.basename(testsuite_path))[0]
            testsuite_id = to_readable_name(base_filename)

            for testcase_result in result_data['testcase_results']:
                print("testcase= ", testcase_result['name'])
                # Extract test case
                testcase_path = testcase_result['name'].replace("\\", "/")
                base_filename = os.path.splitext(os.path.basename(testcase_path))[0]
                # Convert to human-readable → replace underscores with spaces
                testcase_id = to_readable_name(base_filename)
                # Extract Feature
                feature_name = extract_path_segment(testcase_path, int(config.get("feature_index")), humanize=True)
                subfeature_name = extract_path_segment(testcase_path, int(config.get("subfeature_index")), humanize=True)
                actmo_request.append(
                    {
                        "nama_tester": config.get("tester_name"),
                        "fungsi": config.get("function_name"),
                        "project": config.get("project_name"),
                        "platform": config.get("browser"),
                        "fitur": feature_name,
                        "sub_fitur": subfeature_name,
                        "environment": config.get("environment", ""),
                        "id_test": id_test,
                        "date": start_time['date'],
                        "month": start_time['month'],
                        "year": start_time['year'],
                        "start_time": start_time['time'],
                        "end_time": end_time['time'],
                        "testcase_id": testcase_id,
                        "testcase": testcase_path,
                        "testcase_status": testcase_result['status'],
                        "report_folder": report_path,
                        "testsuite_id": testsuite_id,
                        # "testsuite": testsuite_path,
                        "run_type": config.get("run_type"),
                        "uqa":""
                    }
                )
            
        # Do request to actmo
        headers = {
        'Content-Type': 'application/json'
        }
        print("Actmo Request: ", actmo_request)
        try:
            response = requests.post(
                config.get("actmo_url") + "/insert-master-katalon",
                headers=headers,
                data=json.dumps(actmo_request)
            )        
            print("Actmo Response:", response.json())
        except Exception as e:
            print(f"Error occur while retrieving actmo response: {str(e)}")
    else:
        print("result.json not found at:", result_path)