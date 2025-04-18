"""
A simple Flask web application.

This module creates a Flask application instance and defines a single route
for the root URL ('/'). When accessed, the root URL returns a 'Hello, World!'
message.

Functions:
    hello_world(): Returns a 'Hello, World!' message.

Usage:
    Run this module directly to start the Flask development server.
    The server will be accessible at http://127.0.0.1:5000/.

Example:
    $ python app.py
"""

# Import the Flask class from the flask module.
from flask import Flask

# Create a Flask app instance
app = Flask(__name__)

# Define a route for the root URL ('/')
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
