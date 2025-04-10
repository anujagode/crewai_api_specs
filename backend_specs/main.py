#!/usr/bin/env python
from flask import Flask, request, jsonify
from crewai.flow import Flow, start, listen
from pydantic import BaseModel
from typing import Optional
import os
import sys

from process_prd import generate_swagger_from_prd

# ---------- CrewAI Flow State ----------
class SwaggerState(BaseModel):
    prd_file_path: Optional[str] = None
    swagger_file_path: Optional[str] = None


# ---------- CrewAI Swagger Flow ----------
class SwaggerFlow(Flow[SwaggerState]):

    @start()
    def load_prd_file(self):
        print(f"\nChecking PRD file: {self.state.prd_file_path}")
        if not self.state.prd_file_path or not os.path.exists(self.state.prd_file_path):
            raise FileNotFoundError(f"PRD file not found: {self.state.prd_file_path}")

    @listen(load_prd_file)
    def generate_swagger(self):
        print(f"\nGenerating Swagger from PRD: {self.state.prd_file_path}")
        try:
            swagger_path = generate_swagger_from_prd(self.state.prd_file_path)
            self.state.swagger_file_path = swagger_path
            print(f"Swagger file generated at: {swagger_path}")
        except Exception as e:
            print(f"Failed to generate Swagger: {e}")
            raise


# ---------- CLI Entrypoint ----------
def kickoff(prd_path: str):
    flow = SwaggerFlow()
    flow.state.prd_file_path = prd_path
    flow.kickoff()


# ---------- Optional Flask API ----------
app = Flask(__name__)

@app.route('/process_prd', methods=['POST'])
def api_process_prd():
    data = request.json
    prd_file = data.get("prd_file_path")

    if not prd_file or not os.path.exists(prd_file):
        return jsonify({"error": "Invalid or missing PRD file path"}), 400

    try:
        flow = SwaggerFlow()
        flow.state.prd_file_path = prd_file
        flow.kickoff()
        return jsonify({
            "message": "Swagger generated successfully",
            "swagger_file": flow.state.swagger_file_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- Run as Script or Server ----------
if __name__ == "__main__":
    if len(sys.argv) == 2:
        prd_file = sys.argv[1]
        kickoff(prd_file)
    else:
        print("Starting Swagger Flask API server...")
        app.run(port=5001)
