# app.py
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import tempfile
import os
import deepseek_to_pdf

app = Flask(__name__)
CORS(app)

@app.before_request
def log_request():
    app.logger.debug(f"Headers: {dict(request.headers)}")
    app.logger.debug(f"Body preview: {request.get_data()[:200]}...")

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    if not request.content_type.startswith(('multipart/form-data', 'application/json')):
        return jsonify({"error": "Unsupported media type"}), 415

    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "Empty file part"}), 400
            text = file.read().decode('utf-8')
        elif request.is_json:
            text = request.json.get('text', '')
            if not text:
                return jsonify({"error": "Missing text field"}), 400
        else:
            return jsonify({"error": "No valid input provided"}), 400
        
        # Generate PDF
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            output_path = deepseek_to_pdf(text, tmp.name)
            
        return send_file(output_path, mimetype='application/pdf')

    except Exception as e:
        app.logger.error(f"Conversion error: {str(e)}")
        return jsonify({"error": "Invalid request format", "details": str(e)}), 400

    finally:
        if 'tmp' in locals():
            os.unlink(tmp.name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
