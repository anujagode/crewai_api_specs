from crewai import Agent
import openai
import os
from dotenv import load_dotenv

# Load OpenAI API key from .env file
load_dotenv()  # Load the API key from a .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def swagger_generator_agent(extracted_text):
    """Create the Swagger Generator Agent with PRD text input."""
    prompt = f"""
    Based on the following extracted PRD text, generate a comprehensive OpenAPI 3.0.3 Swagger specification:

    --- EXTRACTED PRD TEXT ---
    {extracted_text}
    --- END OF EXTRACTED PRD TEXT ---

    Your task is to:
    1. Analyze the PRD thoroughly and extract API features.
    2. Identify API endpoints, HTTP methods (GET, POST, PUT, DELETE), request/response schemas, and error handling.
    3. Ensure the Swagger YAML follows best practices, including metadata, security schemes, and response examples.

    The Swagger YAML specification should:
    - Include metadata like API title, version, description, and servers.
    - Define all relevant API paths and methods with proper parameters and responses.
    - Include security mechanisms such as OAuth2, API Keys, or JWT authentication if mentioned.
    - Be fully validated according to OpenAPI 3.0.3 standards.
    """
    return Agent(
        name="Swagger Generator",
        role="Expert API Architect & OpenAPI 3.0.3 Specialist",
        goal="Extract API features from the PRD and generate a comprehensive OpenAPI 3.0.3 Swagger specification.",
        backstory=(
            "A highly experienced API architect specializing in OpenAPI 3.0.3 specifications. "
            "With extensive knowledge in RESTful API design, authentication methods, and API documentation standards, "
            "this expert transforms complex PRD documents into well-structured, production-ready Swagger specifications."
        ),
        model="gpt-4-turbo",
        api_key=OPENAI_API_KEY,
        verbose=True,
        context=extracted_text,  # ✅ Pass PRD text dynamically!
        constraints=[
            "Analyze the PRD thoroughly before generating Swagger YAML.",
            "Dynamically extract API endpoints, HTTP methods (GET, POST, PUT, DELETE), and request/response schemas.",
            "Ensure the OpenAPI 3.0.3 YAML follows best practices, including metadata, security schemes, and error handling.",
            "Each endpoint must include correct parameters, request bodies, responses, and applicable HTTP status codes.",
            "Generate reusable data models in the `components` section of the Swagger YAML.",
            "Include security mechanisms such as OAuth2, API Keys, or JWT authentication if mentioned in the PRD.",
            "Ensure comprehensive API documentation with examples, parameter descriptions, and status codes.",
            "Validate that all endpoints adhere to RESTful best practices.",
            "Check for versioning and include a `servers` section with a versioned API base URL.",
            "Include response schemas for 200 (success), 400 (bad request), 404 (not found), and 500 (server error)."
        ],
        expected_output="A structured OpenAPI 3.0.3 YAML specification reflecting the PRD details, including endpoints, authentication, and error handling."
    )
