import logging
import subprocess

# Configure logging for the test script
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

test_cases = [
    {"name": "Under 40 Years Old", "input_file": "tests/under_40_input.json", "expected_error": "Participant's age '39' is less than 40 years old."},
    {"name": "Dates Out of Range", "input_file": "tests/dates_out_of_range_input.json", "expected_error": "Date '2012-12-01' in field 'collection_date' is out of range."},
    {"name": "Fields Exceed Length", "input_file": "tests/fields_length_exceed_input.json", "expected_error": "String 'Genomics Lab Inc........' exceeds 64 characters"},
    {"name": "Invalid UUID", "input_file": "tests/invalid_uuid_input.json", "expected_error": "Invalid participant ID in file name"},
    {"name": "Missing File", "input_file": "tests/missing_file_input.json", "expected_error": "Expected exactly 2 files in"},
    {"name": "Missing context_path", "input_file": "tests/missing_context_path_input.json", "expected_error": "Invalid or missing context path"},
    {"name": "Extra Files", "input_file": "tests/extra_files_input.json", "expected_error": "Expected exactly 2 files in"},
    {"name": "Valid Input", "input_file": "tests/valid_input.json", "expected_error": None},
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