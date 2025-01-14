import os
import sys
import json
import input_handler as input_handler
import process_txt as txt
import validate_and_process_json as json_validate
from datetime import datetime


def main():
    try:
        start_time = datetime.now()
        # Check if the input JSON file is provided as a command-line argument
        if len(sys.argv) < 2:
            raise ValueError("Input JSON file is required as an argument.")

        input_json = sys.argv[1]

        # Validate that the provided file exists
        if not os.path.exists(input_json):
            raise FileNotFoundError(f"Input file does not exist: {input_json}")

        # Load and parse the JSON file
        with open(input_json, 'r') as file:
            input_data = json.load(file)

        # Validate and load input paths
        context_path, results_path = input_handler.validate_and_load_input(input_data)
        print(f"Context Path: {context_path}")
        print(f"Results Path: {results_path}")
        print("Input validation complete. Ready for ETL processing.")

        # Validate the participant files in the context_path
        participant_files = input_handler.validate_context_path_files(context_path, results_path)
        print(f"Validated participant files in: {context_path}")

        # Process the .txt file
        txt_results = txt.process_txt_files(participant_files[".txt"])
        # Process the .json file
        try:
            json_result = json_validate.process_json_files(participant_files[".json"])
            if json_result is None:
                sys.exit(1) # if the processing fails, exit
        except ValueError as e:
            print(f"Validation error in {participant_files['.json']}: {e}")
            sys.exit(1)


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
        # write the merged result into a file in the results_path
        output_file_path = os.path.join(results_path, f"{participant_id}.json")
        with open(output_file_path, 'w') as output_file:
            json.dump(merged_results, output_file, indent=4)


        print(f"Results for participant ID {participant_id} saved to {output_file_path}")
        print("ETL pipeline completed successfully.")

    except ValueError as ve:
        print(f"Validation Error: {ve}")
        sys.exit(1)
    except FileNotFoundError as fnfe:
        print(f"File Error: {fnfe}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()






