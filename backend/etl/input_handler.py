import os
import logging

def validate_input_file(input_data):
    """
    Validate input JSON and ensure paths are correct.

    :param input_data: Parsed input JSON data.
    :return: context_path, results_path.
    """
    logging.info("Validating input JSON structure.")
    try:
        context_path = input_data.get("context_path")
        results_path = input_data.get("results_path")

        # validate context path is included in the input and exists
        if not context_path or not os.path.exists(context_path):
            logging.error(f"Invalid or missing context_path:")
            raise FileNotFoundError(f"Invalid or missing context path: {context_path}")

        # validate result path is given in the input argument
        if not results_path:
            logging.error("Results path is not specified")
            raise ValueError("Results path is not specified.")

        if not results_path.endswith("/out/"):
            logging.error(f"Results path does not end with '/out/'")
            raise ValueError("Results path does not end with '/out/'")

        if not results_path[:-4] == context_path:
            logging.error(f"Results path and context path must share the same base directory: "
                         f"context_path={context_path}, results_path={results_path} ")
            raise ValueError("Context path and results path must share the same base directory")

        logging.info(f"Validation successful for context_path: {context_path}, results_path: {results_path}")
        return context_path, results_path


    except Exception as e:
        logging.error(f"Input validation failed: {e}")
        raise

def validate_context_path_files(context_path, results_path):
    """
    Validate there are exactly two files in the context path, ensure naming conventions.


    :param context_path: Directory containing participant files.
    :param results_path: Directory to save output.
    :return: Dictionary of validated file paths.
    """
    # Initialize a dictionary to store file paths, and a set to validate the uuid id identical for both files
    participant_files = {}
    participant_id_set = set()

    # Get the list of files in the directory
    files = [
        file for file in os.listdir(context_path)
        if os.path.isfile(os.path.join(context_path, file))
        and not file.startswith(".")  # Exclude hidden files like .DS_Store
        and os.path.join(context_path, file) != results_path  # Exclude results_path
    ]

    # Validate that only two files exist
    if len(files) != 2:
        logging.error(f"Expected exactly 2 files in {context_path}, but found {len(files)}.")
        raise ValueError(f"Expected exactly 2 files in {context_path}, but found {len(files)}.")


    for file in files:
        # Validate file extension
        if not file.endswith(('.txt', '.json')):
            logging.error(f"File {file} does not end with '.txt' or '.json'.")
            raise ValueError(f"File {file} does not end with '.txt' or '.json'.")

        # Validate file naming convention: {participant_id}_dna.<extension>
        try:
            participant_id, extension = extract_file_names(file)
        except ValueError as e:
            logging.error(f"Invalid file naming format: {file}")
            raise ValueError(f"Invalid file naming format: {file}") from e

        # Validate the UUID
        if not is_valid_uuid(participant_id):
            logging.error(f"Invalid participant ID in file name: {file}")
            raise ValueError(f"Invalid participant ID in file name: {file}")

        participant_id_set.add(participant_id)
        # Add the file to the dictionary
        participant_files[extension] = os.path.join(context_path, file)

    # validate uuid consistency
    if len(participant_id_set) != 1:
        logging.error(f"Files in {context_path} do not share the same participant ID.")
        raise ValueError(f"Files in {context_path} do not share the same participant ID.")

    # Ensure both .txt and .json files are present
    if '.txt' not in participant_files or '.json' not in participant_files:
        logging.error(f"Missing .txt or .json files in {context_path}")
        raise ValueError(f"Missing .txt or .json file for participant in {context_path}.")

    logging.info(f"Validation successful for files in {context_path}")
    return participant_files

def extract_file_names(file_name):
    """
    Extract the participant ID and extension from the file name.

    :param file_name: File name to parse.
    :return: A tuple (participant_id, extension).
    :raises ValueError: If the file name format is invalid.
    """
    parts = file_name.split('_dna.')
    if len(parts) != 2 or not parts[1] in ('txt', 'json'):
        raise ValueError("Invalid file name format.")
    return parts[0], f".{parts[1]}"

def is_valid_uuid(participant_id):
    """
    Validate that a participant ID is a valid UUID format.

    :param participant_id: The participant ID to validate.
    :return: True if valid, False otherwise.
    """
    return len(participant_id) == 36 and all(c.isalnum() or c == '-' for c in participant_id)













