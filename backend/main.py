from flask import Flask, request, jsonify
import shutil
import os
from process_prd import generate_swagger_from_prd
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

UPLOAD_DIR = "backend/uploads/"
OUTPUT_DIR = "backend/output/"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/upload/', methods=['POST'])
def upload_prd():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.stream, buffer)

    # Process the PRD and generate the Swagger YAML file
    swagger_path = generate_swagger_from_prd(file_path)

    if not swagger_path:
        return jsonify({"error": "Failed to generate Swagger file"}), 500

    return jsonify({"message": "Swagger API file generated", "swagger_file": swagger_path})

if __name__ == '__main__':
    app.run(debug=True)
