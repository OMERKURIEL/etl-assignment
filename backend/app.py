import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

TESTS_DIRECTORY = "./inputs/"  # Directory containing the JSON files

@app.route("/list-files", methods=["GET"])
def list_files():
    """Returns a list of available JSON files in the inputs directory."""
    try:
        files = [f for f in os.listdir(TESTS_DIRECTORY) if f.endswith(".json")]
        return jsonify({"files": files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/run-pipeline", methods=["POST"])
def run_pipeline():
    """
        Runs the ETL pipeline on selected JSON files from the 'inputs' directory.
        Request: JSON with "input_files": a list of filenames to process.
        Process:
            - Validates file existence in 'inputs/'.
            - Runs 'pipeline.py' on each valid file.
            - Captures logs and success/failure status.
        """
    data = request.json # extracts input JSON data from the frontend request
    input_files = data.get("input_files", []) # extract the input file fields from data

    if not input_files:
        return jsonify({"error": "No input files specified"}), 400

    logs = {}
    results = {}

    for input_file in input_files:
        file_path = os.path.join(TESTS_DIRECTORY, os.path.basename(input_file))

        if not os.path.exists(file_path):
            logs[input_file] = f"Error: File {file_path} does not exist."
            continue

        process = subprocess.run(["python", "pipeline.py", file_path], capture_output=True, text=True)

        logs[input_file] = process.stdout or process.stderr
        results[input_file] = "Pipeline completed successfully" if process.returncode == 0 else "Pipeline failed"

    return jsonify({"logs": logs, "results": results})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
