import os

def validate_and_load_input(input_data):
    """
    this method validates the input data, if valid, it returns it as two separate variables
    :param input_data:
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

