import os

def validate_and_load_input(input_data):
    """
    Validates the input data, if valid, it returns it as two separate variables.

    :param input_data: JSON-like input data with context_path and results_path.
    :return: context_path, results_path
    """
    try:
        context_path = input_data.get("context_path")
        results_path = input_data.get("results_path")

        # validate context path is included in the input and exists
        if not context_path or not os.path.exists(context_path):
            raise FileNotFoundError(f"Context path does not exist: {context_path}")

        # validate result path is given in the input argument
        # if the result path doesn't already exist, create this directory
        if not results_path:
            raise ValueError("Results path is not specified.")
        if not os.path.exists(results_path):
            os.makedirs(results_path)

        return context_path, results_path


    except Exception as e:
        print (f"Failed to validate input data: {e}")
        raise

def validate_context_path_files(context_path, results_path):
    """
    Validates the files in the context_path
    Ensures the path contains both .txt and .json files with a valid UUID.

    :param results_path:
    :param context_path: Path to the directory containing the participant's files.
    :return: A dictionary mapping file extensions (.txt, .json) to their file paths.
    """
    # Get the list of files in the directory
    files = [
        file for file in os.listdir(context_path)
        if os.path.isfile(os.path.join(context_path, file))
        and not file.startswith(".")  # Exclude hidden files like .DS_Store
        and os.path.join(context_path, file) != results_path  # Exclude results_path
    ]

    # Validate that only two files exist
    if len(files) != 2:
        raise ValueError(f"Expected exactly 2 files in {context_path}, but found {len(files)}.")

    # Initialize a dictionary to store file paths
    participant_files = {}

    for file in files:
        # Validate file extension
        if not file.endswith(('.txt', '.json')):
            raise ValueError(f"Unsupported file extension found: {file}")

        # Extract UUID (participant_id) from the file name
        participant_id, extension = os.path.splitext(file)

        # Validate the UUID
        if len(participant_id) != 36 or not all(c.isalnum() or c == '-' for c in participant_id):
            raise ValueError(f"Invalid participant ID in file name: {file}")

        # Add the file to the dictionary
        participant_files[extension] = os.path.join(context_path, file)

    # Ensure both .txt and .json files are present
    if '.txt' not in participant_files or '.json' not in participant_files:
        raise ValueError(f"Missing .txt or .json file for participant in {context_path}.")

    return participant_files










