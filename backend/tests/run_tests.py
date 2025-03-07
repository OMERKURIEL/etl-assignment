
import pytest
import subprocess
import os
import json



def run_pipeline(input_file):
    """Run the ETL pipeline and return the process result."""
    result = subprocess.run(["python", "backend/pipeline.py", input_file], capture_output=True, text=True)
    return result

@pytest.mark.parametrize("test_input,expected_error", [
    ("under_40_input.json", "Participant's age '39' is less than 40 years old."),
    ("dates_out_of_range_input.json", "Date '2012-12-01' in field 'collection_date' is out of range."),
    ("fields_length_exceed_input.json", "String 'Genomics Lab Inc.............................................................................' exceeds 64 characters"),
    ("invalid_uuid_input.json", "Invalid participant ID in file name"),
    ("missing_file_input.json", "Expected exactly 2 files in"),
    ("missing_context_path_input.json", "Invalid or missing context path"),
    ("extra_files_input.json", "Expected exactly 2 files in"),
    ("results_path_doesnt_end_with_out.json", "Results path backend/tests/f3324a99-8a63-4ada-9d1d-562f84c76365/res/ does not end with '/out/'"),
    ("paths_doesnt_have_common_uuid.json", "Context path backend/tests/f3324a99-8a63-4ada-9d1d-562f84c76364/ and results path backend/tests/f3324a99-8a63-4ada-9d1d-562f84c76365/out/ must share the same base directory"),
    ("missing_results_path_input.json", "Results path is not specified."),
    ("files_with_incorrect_extension.json", "File f3324a99-8a63-4ada-9d1d-562f84c76311_dna.js does not end with '.txt' or '.json'."),
    ("wrong_naming_convention.json", "Invalid file naming format: f3324a99-8a63-4ada-9d1d-562f84c76312.json"),
    ("context_path_uuid_is_not_as_files_uuid.json", "Context path UUID (f3324a99-8a63-4ada-9d1d-562f84c76315) and participant ID (f3324a99-8a63-4ada-9d1d-562f84c7636d) do not match."),
    ("files_doesnt_have_common_uuid.json", "Files in backend/tests/f3324a99-8a63-4ada-9d1d-562f84c76314/ do not share the same participant ID.")

])
def test_pipeline_edge_cases(test_input, expected_error):
    """Test the ETL pipeline for various edge cases."""
    input_file_path = os.path.join("inputs", test_input)
    result = run_pipeline(input_file_path)

    assert result.returncode != 0, f"Pipeline should fail for {test_input}"
    assert expected_error in result.stderr, f"Expected error '{expected_error}' not found in {test_input} log."

def test_pipeline_success():
    """Test the ETL pipeline with valid input to ensure success."""
    valid_input_file = "inputs/valid_input.json"
    result = run_pipeline(valid_input_file)

    assert result.returncode == 0, "Pipeline should succeed with valid input"
    assert "ETL pipeline completed successfully" in result.stderr, "Pipeline did not complete as expected."

def test_valid_input():
    """
    Test the pipeline with a valid input file.
    """
    input_file = "inputs/valid_input.json"
    result = subprocess.run(
        ["python", "backend/pipeline.py", input_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Pipeline failed: {result.stderr}"
    assert "ETL pipeline completed successfully" in result.stderr, "Pipeline did not complete as expected."

    # Check if the results file is generated
    with open(input_file, 'r') as f:
        input_data = json.load(f)
        results_path = input_data["results_path"]
        participant_id = os.path.basename(os.path.normpath(input_data["context_path"]))
        output_file = os.path.join(results_path, f"{participant_id}.json")

    assert os.path.exists(output_file), f"Expected results file not found at {output_file}"

    # verify the content of the results file
    with open(output_file, 'r') as output_f:
        results_data = json.load(output_f)
        assert results_data["metadata"]["context_path"] == input_data["context_path"], "Context path mismatch in output"
        assert results_data["metadata"]["results_path"] == results_path, "Results path mismatch in output"