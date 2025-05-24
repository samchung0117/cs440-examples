"""
Flask API for KPI and Risk Management Dashboard

This module provides a RESTful API for managing Key Performance Indicators (KPIs),
KPI targets, risks, and user feedback. The API serves JSON data from local files
and supports CORS for cross-origin requests.

Features:
- KPI data retrieval
- KPI targets management
- Risk management (CRUD operations)
- User feedback collection
- Predefined risks handling

Data Storage:
All data is stored in JSON files within the './data' directory:
- kpis.json: KPI metrics data
- kpi_targets.json: KPI target values
- risks.json: Active risk entries
- predefined_risks.json: Template/predefined risk options
- feedback.json: User feedback submissions

Dependencies:
- Flask: Web framework
- flask-cors: Cross-Origin Resource Sharing support
- json: JSON data handling
- os: File system operations
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

DATA_DIR = './data'
KPI_FILE = os.path.join(DATA_DIR, 'kpis.json')
KPI_TARGETS_FILE = os.path.join(DATA_DIR, 'kpi_targets.json')
RISK_FILE = os.path.join(DATA_DIR, 'risks.json')


def read_json(file):
    """
    Read and parse JSON data from a file.
    
    Args:
        file (str): Path to the JSON file to read
        
    Returns:
        dict or list: Parsed JSON data
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    with open(file, 'r') as f:
        return json.load(f)


def write_json(file, data):
    """
    Write data to a JSON file with proper formatting.
    
    Args:
        file (str): Path to the JSON file to write
        data (dict or list): Data to serialize and write to file
        
    Raises:
        IOError: If there's an issue writing to the file
    """
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/api/kpi')
def get_kpis():
    """
    Retrieve all KPI data.
    
    Returns:
        Response: JSON response containing KPI metrics data
        
    HTTP Status Codes:
        200: Success - KPI data retrieved
        500: Internal server error (file read issues)
    """
    return jsonify(read_json(KPI_FILE))


@app.route('/api/kpi_targets')
def get_targets():
    """
    Retrieve KPI target values.
    
    Returns:
        Response: JSON response containing KPI targets data
        
    HTTP Status Codes:
        200: Success - KPI targets retrieved
        500: Internal server error (file read issues)
    """
    return jsonify(read_json(KPI_TARGETS_FILE))


@app.route('/api/risks')
def get_risks():
    """
    Retrieve all active risks.
    
    Returns:
        Response: JSON response containing list of active risks
        
    HTTP Status Codes:
        200: Success - Risk data retrieved
        500: Internal server error (file read issues)
    """
    return jsonify(read_json(RISK_FILE))


@app.route('/api/risks', methods=['POST'])
def add_risk():
    """
    Add a new risk to the active risks list.
    
    This endpoint adds a new risk to risks.json and removes it from
    predefined_risks.json if it exists there (to prevent duplicates).
    
    Request Body:
        JSON object containing risk data with at minimum an 'id' field
        
    Returns:
        Response: JSON response with the added risk data
        
    HTTP Status Codes:
        201: Created - Risk successfully added
        400: Bad request - Invalid JSON or missing required fields
        500: Internal server error (file operation issues)
    """
    new_risk = request.get_json()
    risk_file = './data/risks.json'
    predefined_file = './data/predefined_risks.json'

    # Append to risks.json
    risks = []
    if os.path.exists(risk_file):
        with open(risk_file) as f:
            risks = json.load(f)
    risks.append(new_risk)
    with open(risk_file, 'w') as f:
        json.dump(risks, f, indent=2)

    # Remove from predefined_risks.json
    if os.path.exists(predefined_file):
        with open(predefined_file) as f:
            predefined = json.load(f)
        predefined = [r for r in predefined if r.get('id') != new_risk.get('id')]
        with open(predefined_file, 'w') as f:
            json.dump(predefined, f, indent=2)

    return jsonify(new_risk), 201


@app.route('/api/feedback-submission', methods=['POST'])
def save_metric_feedback():
    """
    Save user feedback for metrics.
    
    Appends new feedback to the feedback.json file, creating the file
    if it doesn't exist.
    
    Request Body:
        JSON object containing feedback data
        
    Returns:
        Response: JSON confirmation message
        
    HTTP Status Codes:
        201: Created - Feedback successfully saved
        400: Bad request - Invalid JSON data
        500: Internal server error (file operation issues)
    """
    feedback = request.get_json()
    filepath = './data/feedback.json'
    if os.path.exists(filepath):
        with open(filepath) as f:
            all_feedback = json.load(f)
    else:
        all_feedback = []

    all_feedback.append(feedback)
    with open(filepath, 'w') as f:
        json.dump(all_feedback, f, indent=2)
    return jsonify({"status": "saved"}), 201


@app.route('/api/predefined_risks', methods=['GET'])
def get_predefined_risks():
    """
    Retrieve predefined risk templates.
    
    Returns a list of predefined risks that can be used as templates
    for creating new risks. Returns an empty list if the file doesn't exist.
    
    Returns:
        Response: JSON response containing list of predefined risks
        
    HTTP Status Codes:
        200: Success - Predefined risks retrieved (may be empty list)
        500: Internal server error (file read issues)
    """
    filepath = './data/predefined_risks.json'
    if not os.path.exists(filepath):
        return jsonify([])  # Return empty list if the file doesn't exist
    with open(filepath) as f:
        risks = json.load(f)
    return jsonify(risks)


if __name__ == '__main__':
    """
    Run the Flask application in debug mode.
    
    Debug mode enables:
    - Automatic reloading on code changes
    - Detailed error messages
    - Interactive debugger
    
    Note: Debug mode should be disabled in production environments.
    """
    app.run(debug=True)