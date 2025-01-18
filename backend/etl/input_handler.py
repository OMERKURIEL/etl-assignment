import os
import logging
import re


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
            raise FileNotFoundError(f"Invalid or missing context path: {context_path}")

        # validate result path is given in the input argument
        if not results_path:
            raise ValueError("Results path is not specified.")

        # validate results path is named "out"
        if not results_path.endswith("/out/"):
            raise ValueError(f"Results path {results_path} does not end with '/out/'")

        # validate results path is a subdirectory of the context path
        results_parent = os.path.dirname(results_path.rstrip('/'))
        if results_parent != context_path.rstrip('/'):
            raise ValueError(
                f"Context path {context_path} and results path {results_path} must share the same base directory")

        # validate that context path and results path is a valid UUID
        context_uuid = extract_uuid_from_path(context_path)
        if not context_uuid:
            raise ValueError(f"{context_path} is not a valid path. Last component must be a valid UUID")


        logging.info(f"Validation successful for context_path: {context_path}, results_path: {results_path}")
        return context_path, results_path

    except Exception as e:
        logging.error(f"Input validation failed: {e}")
        raise


def validate_context_path_files(context_path):
    """
    Validate there are exactly two files in the context path, ensure naming conventions.


    :param context_path: Directory containing participant files.
    :return: Dictionary of validated file paths.
    """
    # initialize a dictionary to store file paths, and a set to validate the uuid id identical for both files
    participant_files = {}
    participant_id_set = set()

    # get the list of files in the directory
    files = [
        file for file in os.listdir(context_path)
        if os.path.isfile(os.path.join(context_path, file))
        and not file.startswith(".")  # Exclude hidden files like .DS_Store
    ]

    # validate that only two files exist
    if len(files) != 2:
        logging.error(f"Expected exactly 2 files in {context_path}, but found {len(files)}.")
        raise ValueError(f"Expected exactly 2 files in {context_path}, but found {len(files)}.")


    for file in files:
        # validate file extension
        if not file.endswith(('.txt', '.json')):
            logging.error(f"File {file} does not end with '.txt' or '.json'.")
            raise ValueError(f"File {file} does not end with '.txt' or '.json'.")

        # validate file naming convention: {participant_id}_dna.<extension>
        try:
            participant_id, extension = extract_file_names(file)
        except ValueError as e:
            logging.error(f"Invalid file naming format: {file}, expecting '_dna' before file extension.")
            raise ValueError(f"Invalid file naming format: {file}") from e
        # validate the UUID
        if not is_valid_uuid(participant_id):
            logging.error(f"Invalid participant ID in file name: {file}")
            raise ValueError(f"Invalid participant ID in file name: {file}")

        participant_id_set.add(participant_id) # add the file to the set
        participant_files[extension] = os.path.join(context_path, file) # add the file to the dictionary

    # validate uuid consistency between both files
    if len(participant_id_set) != 1:
        logging.error(f"Files in {context_path} do not share the same participant ID.")
        raise ValueError(f"Files in {context_path} do not share the same participant ID.")

    # validate uuid consistency between the files and the context path
    context_uuid = extract_uuid_from_path(context_path)
    if context_uuid != participant_id:
        logging.error(f"Context path UUID ({context_uuid}) and participant ID ({participant_id}) do not match.")
        raise ValueError(f"Context path UUID and participant ID do not match.")

    # ensure both .txt and .json files are present
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


def extract_uuid_from_path(path):
    """
    Extract UUID from the last component of a path.

    :param path: Path to extract UUID from
    :return: UUID if valid, None otherwise
    """
    path = path.rstrip('/') # remove trailing slash if exists
    last_component = os.path.basename(path) # get the last component of the path
    return is_valid_uuid(last_component) # check if it's a valid UUID


def is_valid_uuid(participant_id):
    """
    Validate that a participant ID is a valid UUID format.

    :param participant_id: The participant ID to validate.
    :return: True if valid, False otherwise.
    """
    uuid_pattern = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})'
    match = re.search(uuid_pattern, participant_id)
    if match:
        return match.group(1)
    return None















