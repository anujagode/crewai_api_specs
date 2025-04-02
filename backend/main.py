from flask import Flask, jsonify
import os
from process_prd import generate_swagger_from_prd

app = Flask(__name__)

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

    def load_sample_file(self):
        print("\n📦 Loading Sample PRD File...")

        file_path = os.path.join(UPLOAD_DIR, "Sample_Specs.md")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ Sample file not found: {file_path}")

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

    def handle_upload(self):
        self.load_sample_file()
        self.process_prd()

        if not self.state["swagger_path"]:
            return jsonify({"error": "Swagger file generation failed"}), 500

        return jsonify({"message": "Swagger API file generated successfully", "swagger_file": self.state["swagger_path"]})

if __name__ == '__main__':
    with app.app_context():
        prd_processor = PRDProcessing()
        response = prd_processor.handle_upload()
        print(response.get_data(as_text=True))
