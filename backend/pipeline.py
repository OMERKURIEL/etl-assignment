import os
import json
from etl import validate_and_process_json as json_validate, input_handler as input_handler, process_txt as txt
from datetime import datetime
import logging
import sys


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "tests")
LOG_FILE = os.path.join(LOG_DIR, "etl_pipeline.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def extract(input_json):
    """
    Extract input data and validate file paths.

    :param input_json: Path to the input JSON file.
    :return: context_path, results_path, participant_files.
    """
    try:
        logging.info("Starting the extract stage")

        # Raise an error if the input file doesn't exist
        if not os.path.exists(input_json):
            logging.error(f"Input file not found: {input_json}")
            raise FileNotFoundError(f"Input file does not exist: {input_json}")

        # Load and parse the JSON file
        with open(input_json, 'r') as file:
            input_data = json.load(file)
            logging.debug(f"Loaded input JSON: {input_data}")

        # Validate and load input paths
        context_path, results_path = input_handler.validate_input_file(input_data)
        logging.info(f"Validated paths: context_path={context_path}, results_path={results_path}")

        # validate the files existence, format, naming in the context path
        participant_files = input_handler.validate_context_path_files(context_path, results_path)
        logging.info(f"Validated participant files: {participant_files}")
    except ValueError:
        logging.error("Exiting the pipeline due to validation error")
        sys.exit(1)

    return context_path, results_path, participant_files


def transform(participant_files):
    """
    Process the .txt and .json files to generate results.
    if the content of the json file is not as expected, raise an appropriate error and exit the program.

    :param participant_files: Dictionary mapping file extensions to file paths.
    :return: txt_results, json_result.
    """
    logging.info("Starting the Transform stage.")
    # Validate and process the content of the .json file
    try:
        json_result = json_validate.process_json_files(participant_files[".json"])
        if json_result is None:
            logging.error("JSON processing failed.")
            sys.exit(1)  # Exit if the processing fails

        logging.debug(f"Processed JSON results: {json_result}")

    except ValueError:
        logging.error("Exiting the pipeline due to validation error")
        sys.exit(1)

    # Process the .txt file
    try:
        txt_results = txt.process_txt_files(participant_files[".txt"])
        logging.debug(f"Processed TXT results: {txt_results}")

    except ValueError:
        logging.error("Exiting the pipeline due to validation error")
        sys.exit(1)

    logging.info("Transform stage completed successfully.")
    return txt_results, json_result


def load(context_path, results_path, txt_results, json_result, participant_files, start_time):
    """
    Merge and write the transformed results to the output file.

    :param context_path: Path to participant files.
    :param results_path: Path to save the output file.
    :param txt_results: Results from .txt file processing.
    :param json_result: validated and cleansed .json metadata.
    :param participant_files: Dictionary mapping file extensions to file paths.
    :param start_time: Start time of processing the data
    """
    logging.info("Starting the Load stage.")

    # Extract the participant ID from the file name
    participant_id = os.path.splitext(os.path.basename(participant_files[".txt"]))[0]
    if participant_id.endswith("_dna"):
        participant_id = participant_id[:-4]

    # Merge the results
    merged_results = {
        "metadata": {
            "start_at": start_time.isoformat(),
            "end_at": datetime.now().isoformat(),
            "context_path": context_path,
            "results_path": results_path
        },
        "results": [
            {
                "participant": {
                    "_id": participant_id
                },
                "txt": txt_results,
                "JSON": json_result
            }
        ]
    }
    # if the results path doesn't exist, create it
    if not os.path.exists(results_path):
        logging.info(f"creating results directory at {results_path}")
        os.makedirs(results_path)
    # write the merged result into a file in the results_path
    output_file_path = os.path.join(results_path, f"{participant_id}.json")
    with open(output_file_path, 'w') as output_file:
        json.dump(merged_results, output_file, indent=4)

    logging.info(f"Load stage completed successfully. Results saved to {output_file_path}")


def main():
    """
    Main function to execute the ETL pipeline.

    This function follows the Extract, Transform, and Load (ETL) process:
    1. Extract: Reads and validates input JSON data.
    2. Transform: Processes the extracted data, ensuring correct format and structure.
    3. Load: Saves the processed results to the specified output directory.

    Logs the start and end times of execution and handles errors gracefully.
    """
    try:
        logging.info("ETL pipeline started.")
        start_at = datetime.now()
        # Check if the input JSON file is provided as a command-line argument
        if len(sys.argv) < 2:
            logging.error("Input JSON file is required as an argument.")
            raise ValueError("Input JSON file is required as an argument.")

        input_json = sys.argv[1] # extracting the .json file input
        # Validate that the provided file exists
        context_path, results_path, participant_files = extract(input_json)
        # Transform Stage
        txt_results, json_result = transform(participant_files)
        # Load stage
        load(context_path, results_path, txt_results, json_result, participant_files, start_at)

        logging.info("ETL pipeline completed successfully.")

    except ValueError as ve:
        logging.error(f"Validation Error: {ve}")
        logging.error("Pipeline exiting due to validation error")
        sys.exit(1)

    except FileNotFoundError as fnfe:
        logging.error(f"File Error: {fnfe}")
        logging.error("Pipeline exiting due to validation error")
        sys.exit(1)

    except Exception as e:
        logging.error(f"Unexpected Error: {e}", exc_info=True)
        logging.error("Pipeline exiting due to an unexpected error")
        sys.exit(1)


if __name__ == "__main__":
    main()






