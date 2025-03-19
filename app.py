# app.py
from flask import Flask, request, send_file
from flask_cors import CORS
import tempfile
import os

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    try:
        # Get input from either text or file
        if 'file' in request.files:
            file = request.files['file']
            text = file.read().decode('utf-8')
        else:
            text = request.json.get('text', '')
        
        # Generate PDF
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            output_path = deepseek_to_pdf(text, tmp.name)
            
        return send_file(output_path, mimetype='application/pdf')

    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        if 'tmp' in locals():
            os.unlink(tmp.name)

if __name__ == '__main__':
    app.run(port=5000)
