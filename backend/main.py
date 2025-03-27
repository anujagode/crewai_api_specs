from flask import Flask, request, jsonify
import shutil
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
from process_prd import generate_swagger_from_prd

app = Flask(__name__)

CORS(app)

UPLOAD_DIR = "backend/uploads/"
OUTPUT_DIR = "backend/output/"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

class PRDProcessing:
    def __init__(self):
        self.state = {
            "file_path": None,
            "swagger_path": None
        }

    def upload_prd(self, file):
        print("\n📦 Uploading PRD File...")

        filename = secure_filename(file.filename)  # Secure the file name
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.stream, buffer)
        
        self.state["file_path"] = file_path

    def process_prd(self):
        print("\n🔄 Processing PRD to Generate Swagger...")

        file_path = self.state["file_path"]
        
        try:
            swagger_path = generate_swagger_from_prd(file_path)
            self.state["swagger_path"] = swagger_path
        except Exception as e:
            print(f"Error processing PRD: {e}")
            return jsonify({"error": "Failed to process PRD"}), 500

    def handle_upload(self, file):
        self.upload_prd(file)
        self.process_prd()

        if not self.state["swagger_path"]:
            return jsonify({"error": "Swagger file generation failed"}), 500

        return jsonify({"message": "Swagger API file generated successfully", "swagger_file": self.state["swagger_path"]})

@app.route('/upload/', methods=['POST'])
def upload_prd():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file provided"}), 400

        prd_processor = PRDProcessing()
        response = prd_processor.handle_upload(file)
        return response
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
