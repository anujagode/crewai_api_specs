from crewai import Agent
import openai
import os
from dotenv import load_dotenv

load_dotenv()  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def validation_agent(extracted_text, swagger_yaml):
    """Create the Swagger Validation Agent."""
    prompt = f"""
You are an expert in validating OpenAPI 3.0.3 Swagger YAML documentation against product requirement documents (PRDs).

--- PRD START ---
{extracted_text}
--- PRD END ---

--- SWAGGER YAML START ---
{swagger_yaml}
--- SWAGGER YAML END ---

Task:
- Validate the Swagger YAML against OpenAPI 3.0.3 specs.
- Ensure **all** APIs mentioned in the PRD are implemented in the Swagger.
- Check that request and response schemas match the requirements described in the PRD.
- Confirm correct use of HTTP methods and endpoint structures.
- Validate response codes and schema references.
- Ensure proper formatting, indentation, and adherence to OpenAPI 3.0.3.

Only return validation result and critical issues. No extra explanation.
"""

    return Agent(
        name="Swagger Validation Agent",
        role="Validates Swagger YAML for coverage and OpenAPI 3.0.3 compliance.",
        goal="Ensure Swagger spec fully aligns with the PRD and OpenAPI 3.0.3 standards.",
        backstory=(
            "An expert OpenAPI and system documentation validator. "
            "They validate Swagger files against real product needs and specification standards."
        ),
        model="gpt-4-turbo",  
        api_key=OPENAI_API_KEY,
        temperature=0.2,
        verbose=True,
        context=swagger_yaml,
        constraints=[
            "Ensure Swagger YAML includes all APIs described in PRD.",
            "Check for correct methods, request/response models, and endpoint completeness.",
            "Verify formatting, structure, and OpenAPI 3.0.3 compliance.",
            "Return validation summary and uncovered APIs or mismatches.",
        ],
        expected_output="Validation summary confirming OpenAPI 3.0.3 compliance and PRD coverage."
    )
