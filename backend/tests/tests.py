import logging
import subprocess

# Configure logging for the test script
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend/tests/etl_pipeline.log"),
        logging.StreamHandler()
    ]
)

test_cases = [
    {"name": "Under 40 Years Old", "input_file": "inputs/under_40_input.json", "expected_error": "Participant's age '39' is less than 40 years old."},
    {"name": "Dates Out of Range", "input_file": "inputs/dates_out_of_range_input.json", "expected_error": "Date '2012-12-01' in field 'collection_date' is out of range."},
    {"name": "Fields Exceed Length", "input_file": "inputs/fields_length_exceed_input.json", "expected_error": "String 'Genomics Lab Inc.............................................................................' exceeds 64 characters"},
    {"name": "Invalid UUID", "input_file": "inputs/invalid_uuid_input.json", "expected_error": "Invalid participant ID in file name"},
    {"name": "Missing File", "input_file": "inputs/missing_file_input.json", "expected_error": "Expected exactly 2 files in"},
    {"name": "Missing context_path", "input_file": "inputs/missing_context_path_input.json", "expected_error": "Invalid or missing context path"},
    {"name": "Missing results_path", "input_file": "inputs/missing_results_path_input.json", "expected_error": "Results path is not specified"},
    {"name": "Extra Files", "input_file": "inputs/extra_files_input.json", "expected_error": "Expected exactly 2 files in"},
    {"name": "paths doesnt have same uuid", "input_file": "inputs/paths_doesnt_have_common_uuid.json", "expected_error": "Input validation failed: Context path backend/tests/f3324a99-8a63-4ada-9d1d-562f84c76364/ and results path backend/tests/f3324a99-8a63-4ada-9d1d-562f84c76365/out/ must share the same base directory"},
    {"name": "results path doesnt end with out", "input_file": "inputs/results_path_doesnt_end_with_out.json", "expected_error": "Input validation failed: Results path backend/tests/f3324a99-8a63-4ada-9d1d-562f84c76365/res/ does not end with '/out/'"},
    {"name": "wrong naming convention", "input_file": "inputs/wrong_naming_convention.json", "expected_error": "Invalid file naming format: f3324a99-8a63-4ada-9d1d-562f84c76312.json"},
    {"name": "files with incorrect extensions", "input_file": "inputs/files_with_incorrect_extension.json", "expected_error": "File f3324a99-8a63-4ada-9d1d-562f84c76311_dna.js does not end with '.txt' or '.json'"},
    {"name": "context path uuid is not as files uuid", "input_file": "inputs/context_path_uuid_is_not_as_files_uuid.json", "expected_error": "Context path UUID (f3324a99-8a63-4ada-9d1d-562f84c76315) and participant ID (f3324a99-8a63-4ada-9d1d-562f84c7636d) do not match."},
    {"name": "files doesnt have common uuid", "input_file": "inputs/files_doesnt_have_common_uuid.json", "expected_error": " Files in backend/tests/f3324a99-8a63-4ada-9d1d-562f84c76314/ do not share the same participant ID."},
    {"name": "Valid Input", "input_file": "inputs/valid_input.json", "expected_error": None},
]


for test in test_cases:
    logging.info(f"Running Test: {test['name']}")
    result = subprocess.run(
        ["python", "backend/pipeline.py", test["input_file"]],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        if test["expected_error"] in result.stderr:
            logging.info(f"Test {test['name']} failed as expected with the following logs:\n{result.stderr.strip()}")
        else:
            logging.error(f"Test {test['name']} failed with unexpected error logs:\n{result.stderr.strip()}")
    else:
        logging.info(f"Test {test['name']} passed! \n{result.stderr.strip()}")

    logging.info("-" * 50)