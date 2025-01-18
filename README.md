# **ETL Pipeline for Genetic Data Processing**

This project is an ETL (Extract, Transform, Load) pipeline designed for processing genomic data. 
The pipeline performs data extraction, validation, and transformation from structured .json and .txt files, and loads it to a path given as an argument.
Additionally, a bonus frontend interface is included for easy interaction, though the core logic resides in the backend processing.

## Project Structure:
```plaintext
etl-assignment/
│── backend/                       # Backend ETL pipeline (core logic)
│   │── pipeline.py                 # Main ETL execution script
│   │── etl/                       # ETL processing modules
│   │   │── input_handler.py       # Handles input validation & file structure checks
│   │   │── validate_and_process_json.py # Validates & processes JSON metadata
│   │   │── process_txt.py         # Processes DNA sequences from TXT files
│   │── tests/                     # Test scripts and test cases for the pipeline
│   │── app.py                     # Flask API for running ETL from frontend
│── frontend/                       # (Bonus) React-based UI
│   │── src/                        # React components
│   │── public/                     # Static frontend assets
│   │── package.json                # Frontend dependencies
│   │── webpack.config.js           # Webpack configuration for frontend
│── inputs/                         # Pre-existing sample input files
│── venv/                           # Virtual environment (not included in Git)
│── requirements.txt                # Python dependencies
│── README.md                       # Documentation (this file)
```
### Overview:
The pipeline.py orchestrate the ETL process, calling 3 methods - extract, transform, load. 
- Extract method: calls 2 method in the input_handler.py validating the input .json file
- Transform method: calls 2 methods:
  - validate_and_process_json_files
  - process_txt_files
- Load method:
  - merging the processes files into a .json file, creating the output directory if it doesn't exist and loading the file to the directory.
    


## Installation & Setup:

Follow these steps to set up the backend ETL pipeline and the optional frontend UI.

 ### Backend Setup:
#### Prerequisites

1. [ ] Python 3.8+ installed
2. [ ] pip package manager


#### **Installation**:
- Clone the repository:
    `git clone https://github.com/OMERKURIEL/etl-assignment.git`
- Move to the cloned directory:
   ` cd etl-assignment`
- Create a virtual environment and activate it:
    `python -m venv venv`
    `source venv/bin/activate`  # On Windows: venv\Scripts\activate
- Install dependencies:
    `pip install -r requirements.txt`

#### Running the ETL Pipeline:

- To process an input file manually:
- from the etl-assignment directory run:
    `python backend/pipeline.py inputs/valid_input.json`

This will validate, transform, and load genomic data from the input file.

##### Running tests:
- from the etl-assignment directory, run unit tests for input validation and ETL logic:

    `pytest backend/tests/run_tests.py`
    `python backend/tests/tests.py`
### (Optional) Frontend Setup:
#### Prerequisites

1. [ ] Node.js (v16+) installed
2. [ ] npm package manager

##### **Installation & Running the UI**:
1. nNavigate to the frontend folder `cd frontend`
2. Install dependencies `npm install`
3. Start the frontend development server: `npm start`
4. In an additional terminal, Navigate to the backend folder 
5. Start the backend development server `python app.py`

The interface should now be accessible at http://localhost:3000




















