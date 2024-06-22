from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/api/stats', methods=['POST'])
def calculate_stats():
    data = request.json

    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Invalid request. Please send JSON data."}), 400

    # Check if 'numbers' key exists in the JSON data
    if not data or 'numbers' not in data:
        return jsonify({"error": "Invalid input. Please provide a 'numbers' key with a list of numbers."}), 400

    numbers = data['numbers']

    # Check if the input is a list
    if not isinstance(numbers, list):
        return jsonify({"error": "Invalid input. 'numbers' must be a list."}), 400

    # Check if the list is not empty
    if len(numbers) == 0:
        return jsonify({"error": "Invalid input. The list of numbers cannot be empty."}), 400

    try:
        # Convert all numbers to float
        numbers = [float(num) for num in numbers]

        # Check for NaN or Infinity values
        if any(not np.isfinite(num) for num in numbers):
            return jsonify({"error": "Invalid input. Please provide only finite numbers."}), 400

        stats = {
            'count': len(numbers),
            'mean': float(np.mean(numbers)),
            'median': float(np.median(numbers)),
            'std_dev': float(np.std(numbers)),
            'min': float(np.min(numbers)),
            'max': float(np.max(numbers))
        }
        return jsonify(stats), 200

    except ValueError as e:
        return jsonify({"error": f"Invalid input. {str(e)}"}), 400
    except Exception as e:
        # Log the exception here if you have logging set up
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found. Please check the API endpoint."}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed. Please use POST for this endpoint."}), 405

if __name__ == '__main__':
    app.run(debug=True, port=5000)