import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # backend/
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # home_assignment/
TESTS_DIRECTORY = os.path.join(ROOT_DIR, "inputs")  # home_assignment/inputs/

@app.route("/list-files", methods=["GET"])
def list_files():
    """Returns a list of available JSON files in the inputs directory."""
    try:
        files = [f for f in os.listdir(TESTS_DIRECTORY) if f.endswith(".json")]
        return jsonify({"files": files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/run-pipeline", methods=["POST"])
@app.route("/run-pipeline", methods=["POST"])
def run_pipeline():
    """
    Runs the ETL pipeline on selected JSON files from the 'inputs' directory.
    Converts file paths to absolute before running.
    """
    data = request.json
    input_files = data.get("input_files", [])

    if not input_files:
        return jsonify({"error": "No input files specified"}), 400

    logs = {}
    results = {}

    for input_file in input_files:
        file_path = os.path.join(TESTS_DIRECTORY, input_file)

        print(f" Debug: Processing {input_file} -> Full Path: {file_path}")  # <--- PRINT PATH

        if not os.path.exists(file_path):
            logs[input_file] = f"Error: File {file_path} does not exist."
            continue

        process = subprocess.run(
            ["python", "backend/pipeline.py", file_path],
            capture_output=True,
            text=True,
            cwd=ROOT_DIR,  # ✅ Ensuring correct working directory
        )

        logs[input_file] = process.stdout or process.stderr
        results[input_file] = "Pipeline completed successfully" if process.returncode == 0 else "Pipeline failed"

    return jsonify({"logs": logs, "results": results})




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
