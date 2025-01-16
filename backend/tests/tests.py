import logging
import subprocess

# Configure logging for the test script
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("tests/etl_pipeline.log"),  # Save logs to a file
        logging.StreamHandler() # Also print logs to console
    ]
)

test_cases = [
    {"name": "Under 40 Years Old", "input_file": "inputs/under_40_input.json", "expected_error": "Participant's age '39' is less than 40 years old."},
    {"name": "Dates Out of Range", "input_file": "inputs/dates_out_of_range_input.json", "expected_error": "Date '2012-12-01' in field 'collection_date' is out of range."},
    {"name": "Fields Exceed Length", "input_file": "inputs/fields_length_exceed_input.json", "expected_error": "String 'Genomics Lab Inc........' exceeds 64 characters"},
    {"name": "Invalid UUID", "input_file": "inputs/invalid_uuid_input.json", "expected_error": "Invalid participant ID in file name"},
    {"name": "Missing File", "input_file": "inputs/missing_file_input.json", "expected_error": "Expected exactly 2 files in"},
    {"name": "Missing context_path", "input_file": "inputs/missing_context_path_input.json", "expected_error": "Invalid or missing context path"},
    {"name": "Extra Files", "input_file": "inputs/extra_files_input.json", "expected_error": "Expected exactly 2 files in"},
    {"name": "path doesnt have same uuid", "input_file": "inputs/paths_doesnt_have_common_uuid.json", "expected_error": "Results path and context path must share the same base directory"},
    {"name": "results path doesnt end with out", "input_file": "inputs/results_path_doesnt_end_with_out.json", "expected_error": "Results path does not end with '/out/'"},
    {"name": "Valid Input", "input_file": "inputs/valid_input.json", "expected_error": None},
]

# Run tests
for test in test_cases:
    logging.info(f"Running Test: {test['name']}")
    result = subprocess.run(
        ["python", "pipeline.py", test["input_file"]],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        if test["expected_error"] in result.stderr:
            logging.info(f"Test {test['name']} failed as expected with error: {result.stderr.strip()}")
        else:
            logging.error(f"Test {test['name']} failed with unexpected error: {result.stderr.strip()}")
    else:
        logging.info(f"Test {test['name']} passed unexpectedly!")

    logging.info("-" * 50)