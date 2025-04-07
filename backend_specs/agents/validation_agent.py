from crewai import Agent
import openai
import os
from dotenv import load_dotenv

# Load OpenAI API key from .env file
load_dotenv()  # Load the API key from a .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def validation_agent(swagger_yaml):
    """Create the Swagger Validation Agent."""
    return Agent(
        name="Swagger Validation Agent",
        role="Validates generated Swagger (OpenAPI) YAML file.",
        goal="Validate the Swagger YAML file against OpenAPI 3.0 standards, ensuring it adheres to required structure, data types, and security standards.",
        backstory=(
            "A highly skilled API architect with a deep understanding of OpenAPI 3.0 standards and API validation. "
            "Experienced in ensuring that API documentation meets all specifications and provides clear, consistent, and accurate information to developers and consumers."
        ),
        model="gpt-4-turbo",  # Can use GPT-3.5 or GPT-4 models for validation tasks
        api_key=OPENAI_API_KEY,
        temperature=0.2,
        verbose=True,
        context=swagger_yaml,
        constraints=[
            "Ensure the Swagger YAML follows OpenAPI 3.0.3 standards.",
            "Validate that all paths, methods, and response codes are correctly defined and match the API requirements.",
            "Check for consistency and completeness in request/response models, including properties, data types, and validation rules.",
            "Ensure that all authentication and authorization details (OAuth, API Key, etc.) are correctly included.",
            "Verify that error responses are properly documented with status codes (400, 404, 500) and example messages.",
            "Ensure the Swagger file includes metadata such as title, version, description, and contact info.",
        ],
        expected_output="A validated and error-free Swagger YAML file, fully compliant with OpenAPI 3.0.3 standards."
    )
