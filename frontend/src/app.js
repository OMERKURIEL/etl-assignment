import React, { useState, useEffect } from "react";
import "./app.css";


function App() {
    const [files, setFiles] = useState([]); // Store available JSON files
    const [selectedFiles, setSelectedFiles] = useState([]); // Store selected files
    const [logs, setLogs] = useState({});
    const [results, setResults] = useState({});


    // Fetch available JSON files from backend
    useEffect(() => {
        fetch("http://127.0.0.1:5001/list-files") //calls backend API
            .then(response => response.json())//convert response to json
            .then(data => {
                if (data.files) {
                    setFiles(data.files); // stores files list in state
                }
            })
            .catch(error => console.error("Error fetching files:", error));
    }, []);

    // Handle multiple file selection
function handleFileChange(e) {
    const selectedOptions = Array.from(e.target.selectedOptions).map(option => option.value);
    setSelectedFiles(selectedOptions);
}

    // Run ETL pipeline for selected files
const runPipeline = async () => {
    if (selectedFiles.length === 0) {
        alert("Please select at least one file.");
        return;
    }

    const response = await fetch("http://127.0.0.1:5001/run-pipeline", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input_files: selectedFiles }),  // ✅ Only filenames, not paths
    });

    const data = await response.json();
    setLogs(data.logs || {});
    setResults(data.results || {});
};

    return (
        <div className="app-container">
            <header className="navbar">
                <h1>Pheno.AI</h1>
                <nav>
                </nav>
            </header>

            <main className="content">
                <div className="upload-section">
                    <label>Select files:</label>
                    <select
                        multiple={true}
                        value={selectedFiles}
                        onChange={handleFileChange}
                        size="5"
                    >
                        {files.map((file, index) => (
                            <option key={index} value={file}>
                                {file}
                            </option>
                        ))}
                    </select>
                    <button onClick={runPipeline}>Run Pipeline</button>
                </div>

                <div className="results-section">
                    <h2>Pipeline Results</h2>
                    {Object.entries(results).map(([file, result]) => (
                        <div key={file}>
                            <h3>{file}</h3>
                            <pre>{JSON.stringify(result, null, 2)}</pre>
                        </div>
                    ))}

                    <h2>Pipeline Logs</h2>
                    {Object.entries(logs).map(([file, log]) => (
                        <div key={file}>
                            <h3>{file}</h3>
                            <pre>{log}</pre>
                        </div>
                    ))}
                </div>
            </main>
        </div>
    );
}

export default App;
