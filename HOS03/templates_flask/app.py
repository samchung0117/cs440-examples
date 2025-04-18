"""
A Flask web application that renders an HTML template.

This module creates a Flask application instance and defines a single route
for the root URL ('/'). When accessed, the root URL renders the 'home.html'
template and passes a 'username' variable to it.

Functions:
    home(): Renders the 'home.html' template with a 'username' variable.

Usage:
    Run this module directly to start the Flask development server.
    The server will be accessible at http://127.0.0.1:5000/.

Example:
    $ python app.py

HTML Template:
    Ensure there is a 'home.html' file in a 'templates' folder within the
    project directory. The template should use the 'username' variable to
    display a personalized message.
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    name = "User"
    return render_template('home.html', username=name)

if __name__ == '__main__':
    app.run(debug=True)
