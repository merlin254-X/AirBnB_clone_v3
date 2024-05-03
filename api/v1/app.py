#!/usr/bin/env python3
"""Simple Flask Application"""

from flask import Flask, jsonify
from flask_cors import CORS  # Importing CORS
from models import storage
from os import getenv
from api.v1.views import app_views

# Create the Flask app instance
app = Flask(__name__)

# Register the app's blueprint for API views
app.register_blueprint(app_views)

# Enable CORS for all origins
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Avoid requiring a trailing slash in URLs
app.url_map.strict_slashes = False

# Cleanup resource at the end of each request
@app.teardown_appcontext
def cleanup(_):
    """Close the storage connection"""
    storage.close()

# Handle 404 errors with a custom JSON response
@app.errorhandler(404)
def not_found(_):
    """Return a JSON response for 404 errors"""
    return jsonify({"error": "Not found"}), 404

# Main entry point for the Flask app
if __name__ == "__main__":
    # Retrieve host and port from environment variables, with defaults
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    
    # Start the Flask app with specified host and port
    app.run(host=host, port=port, threaded=True)
