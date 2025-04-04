import os
import fitz  # PyMuPDF for PDF parsing
from crew import SwaggerCrew

OUTPUT_DIR = "backend/output/"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF."""
    try:
        doc = fitz.open(pdf_path)
        return "\n".join([page.get_text("text") for page in doc])
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""

def extract_text_from_md(md_path):
    """Extract text from Markdown."""
    try:
        with open(md_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"❌ Error reading Markdown file: {e}")
        return ""
    
def get_last_n_words(text, n=4000):
    """Returns the last n words from the given text."""
    words = text.split()
    last_n_words = words[-n:]
    return ' '.join(last_n_words)


def extract_text_from_file(file_path):
    """Extract text from PRD (Markdown or PDF)."""
    print(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    print(ext)
    extractors = {".pdf": extract_text_from_pdf, ".md": extract_text_from_md}
    
    if ext in extractors:
        text = extractors[ext](file_path)
        if not text.strip():
            print(f"⚠️ Warning: Extracted text from {file_path} is empty!")
        return get_last_n_words(text, 4000)
    else:
        raise ValueError(f"❌ Unsupported file format: {ext}")

def generate_swagger_from_prd(file_path):
    """Processes PRD and generates Swagger YAML."""
    extracted_text = extract_text_from_file(file_path)
    print(f"Extracted text: {extracted_text}...")  

    # Initialize SwaggerCrew
    swagger_crew = SwaggerCrew()
    prd_processing_crew = swagger_crew.create_prd_processing_crew(extracted_text)
    
    try:
        swagger_yaml = prd_processing_crew.kickoff()  # ✅ Extract API data
    except TypeError as e:
        print(f"❌ Error generating Swagger YAML: {e}")
        return None
    
    if hasattr(swagger_yaml, 'result'):
        swagger_yaml = swagger_yaml.result  
    else:
        swagger_yaml = str(swagger_yaml)

    # ✅ Validate Swagger YAML
    validation_crew = swagger_crew.create_validation_crew(swagger_yaml)
    try:
        validation_result = validation_crew.kickoff()  
    except TypeError as e:
        print(f"❌ Error validating Swagger YAML: {e}")
        return None

    if hasattr(validation_result, "is_valid") and not validation_result.is_valid:
        print(f"❌ Validation failed: {validation_result.errors}")
        return None

    # ✅ Save to output file
    output_file = os.path.join(OUTPUT_DIR, "swagger_api.yaml")
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(swagger_yaml)
        print(f"✅ Swagger file saved: {output_file}")
    except Exception as e:
        print(f"❌ Failed to write Swagger file: {e}")

    return output_file
