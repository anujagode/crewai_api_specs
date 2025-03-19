import os
import openai
import fitz  # PyMuPDF for PDF parsing
from crew import prd_processing_crew, validation_crew
from agents import swagger_generator_agent, validation_agent

OUTPUT_DIR = "backend/output/"

os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists

def extract_text_from_pdf(pdf_path):
    """Extract readable text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def extract_text_from_file(file_path):
    """Extract text from various document types (PDF, TXT, etc.)."""
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def generate_swagger_from_prd(file_path):
    """Reads a PRD file, processes it, and generates Swagger YAML."""
    file_extension = os.path.splitext(file_path)[1].lower()

    # Step 1: Extract Text from PRD file
    extracted_text = extract_text_from_file(file_path)
    print(f"Extracted text: {extracted_text[:1000]}...")  # Print first 1000 characters for debugging

    # Step 2: Pass the extracted text to swagger_generator_agent for Swagger generation
    swagger_generator_agent.goal = f"Generate a detailed Swagger file from the extracted PRD features. Here is the PRD text:\n\n{extracted_text}"

    # Step 3: Generate Swagger YAML
    swagger_yaml = prd_processing_crew.kickoff({})

    # Step 4: Get the Swagger YAML from the output of the crew
    swagger_yaml = str(swagger_yaml.result) if hasattr(swagger_yaml, "result") else str(swagger_yaml)

    if not swagger_yaml.strip():
        print("❌ OpenAI response is empty or invalid!")
        return None

    # Step 5: Validate the Swagger YAML using the validation agent
    validation_result = validation_crew.kickoff({"swagger_yaml": swagger_yaml})  # Validation task

    print(f"Validation Result: {validation_result}")

    if hasattr(validation_result, "is_valid") and not validation_result.is_valid:
        print(f"❌ Validation failed: {validation_result.errors}")
        return None

    # Step 6: Write Swagger YAML to output file
    output_file = os.path.join(OUTPUT_DIR, "swagger_api.yaml")
    
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(swagger_yaml)
        print(f"✅ Swagger file successfully written to {output_file}")
    except Exception as e:
        print(f"❌ Failed to write Swagger file: {e}")

    return output_file
