import os
import subprocess

def run_test(test_name, input_json_path):
    print(f"Running Test: {test_name}")
    try:
        subprocess.run(["python", "etl.py", input_json_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Test {test_name} failed as expected with error:\n{e}")
    print("-" * 50)

# Define test cases
tests = [
    ("Under 40 Years Old", "./tests/under_40_input.json"),
    ("Dates Out of Range", "./tests/dates_out_of_range_input.json"),
    ("Fields Exceed 64 Characters", "./tests/fields_length_exceed_input.json"),
    ("Invalid UUID", "./tests/invalid_uuid_input.json"),
    ("Missing File", "./tests/missing_file_input.json"),
    ("Missing context_path", "./tests/missing_context_path_input.json"),
    ("Extra Files", "./tests/extra_files_input.json"),
]

# Run all tests
for test_name, input_json_path in tests:
    run_test(test_name, input_json_path)
