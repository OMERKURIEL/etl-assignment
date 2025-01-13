import os
import sys
import json
from input_handler import validate_and_load_input
import process_txt as txt
import validate_and_process_json as json_validate


def main():
    try:
        # Check if the input JSON file is provided as a command-line argument
        if len(sys.argv) < 2:
            raise ValueError("Input JSON file path is required as an argument.")

        input_json = sys.argv[1]
        # Validate that the provided file exists
        if not os.path.exists(input_json):
            raise FileNotFoundError(f"Input file does not exist: {input_json}")

        # Load and parse the JSON file
        with open(input_json, 'r') as file:
            input_data = json.load(file)

        # Validate and load input paths
        context_path, results_path = validate_and_load_input(input_data)

        # Proceed with ETL logic (to be implemented later)
        print(f"Context Path: {context_path}")
        print(f"Results Path: {results_path}")
        print("Input validation complete. Ready for ETL processing.")


        

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()






