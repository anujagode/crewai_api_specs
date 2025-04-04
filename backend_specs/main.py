from flask import Flask, request, jsonify
import os
import sys
from process_prd import generate_swagger_from_prd

app = Flask(__name__)

UPLOAD_DIR = "backend/uploads/"
OUTPUT_DIR = "backend/output/"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

class PRDProcessing:
    def __init__(self, prd_file_path):
        self.state = {
            "file_path": prd_file_path,
            "swagger_path": None
        }

    def process_prd(self):
        """Processes the PRD file and generates Swagger API specifications."""
        print(f"\n🔄 Processing PRD file: {self.state['file_path']}")

        if not os.path.exists(self.state["file_path"]):
            print(f"❌ Error: PRD file not found: {self.state['file_path']}")
            return None

        try:
            swagger_path = generate_swagger_from_prd(self.state["file_path"])
            self.state["swagger_path"] = swagger_path
            print(f"\n✅ Swagger API file generated: {swagger_path}")
            return swagger_path
        except Exception as e:
            print(f"❌ Error processing PRD: {e}")
            return None

@app.route('/process_prd', methods=['POST'])
def process_uploaded_prd():
    """API endpoint to process an uploaded PRD file."""
    data = request.json
    prd_file_path = data.get("prd_file_path")

    if not prd_file_path or not os.path.exists(prd_file_path):
        return jsonify({"error": "Invalid PRD file path!"}), 400

    processor = PRDProcessing(prd_file_path)
    swagger_path = processor.process_prd()

    if not swagger_path:
        return jsonify({"error": "Swagger file generation failed"}), 500

    return jsonify({"message": "Swagger API file generated successfully", "swagger_file": swagger_path})

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ Error: No PRD file provided!")
        print("Usage: python3 main.py /path/to/prd_document.md")
        sys.exit(1)

    prd_file_path = sys.argv[1]
    processor = PRDProcessing(prd_file_path)
    swagger_path = processor.process_prd()

    if swagger_path:
        print(f"\n✅ Swagger API file generated successfully: {swagger_path}")
    else:
        print("❌ Swagger API file generation failed!")
