from crewai import Agent
import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def swagger_generator_agent(extracted_text):
    """Create the Swagger Generator Agent with PRD text input."""
    prompt = f"""
You are an expert in designing OpenAPI 3.0.3 specifications. 

Your task is to read the PRD and generate a complete Swagger YAML (OpenAPI 3.0.3) document.

--- PRD CONTENT START ---
{extracted_text}
--- PRD CONTENT END ---

Based on the PRD content above:

Generate a production-ready OpenAPI 3.0.3 YAML that includes:

1. **API Metadata**:
   - Title, version, description, and server URL

2. **Paths and Methods**:
   - Include all mentioned API endpoints
   - Define supported HTTP methods (GET, POST, PUT, DELETE)
   - Each method should include:
     - Summary and description
     - Parameters (query/path/header if any)
     - Request body (if applicable)
     - Responses (200, 400, 404, 500)
     - Examples where appropriate

3. **Components**:
   - Define reusable schemas for request/response bodies
   - Include error response schemas if applicable

4. **Validation**:
   - Ensure the YAML is valid OpenAPI 3.0.3
   - Use proper indentation and structure
   - Avoid extra explanation or comments — return only YAML

Format strictly as a clean OpenAPI YAML file — no prose or extra instructions.
    """

    return Agent(
        name="Swagger Generator",
        role="Expert API Architect & OpenAPI 3.0.3 Specialist",
        goal="Generate a clean, structured OpenAPI 3.0.3 Swagger YAML specification from PRD input.",
        backstory=(
            "A highly skilled API architect with deep knowledge of RESTful APIs and OpenAPI specifications. "
            "They convert vague product requirements into production-ready Swagger YAML documentation "
            "that adheres to OpenAPI 3.0.3 best practices, including reusable components and examples."
        ),
        model="gpt-4-turbo",
        api_key=OPENAI_API_KEY,
        temperature=0.2,
        verbose=True,
        context=prompt,
        constraints=[
            "Return only valid OpenAPI 3.0.3 YAML, nothing else.",
            "Ensure paths, methods, and components are well-structured.",
            "Use proper indentation and spacing for YAML validity.",
            "All responses must include proper status codes and schema references.",
            "Do not add security definitions.",
            "Avoid generic boilerplate — derive all details from PRD.",
        ],
        expected_output="A fully structured and validated OpenAPI 3.0.3 YAML file based on PRD content."
    )
