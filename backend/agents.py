from crewai import Agent
import openai
import os
from dotenv import load_dotenv

# Load OpenAI API key from .env file
load_dotenv()  # Load the API key from a .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Swagger Generation Agent
swagger_generator_agent = Agent(
    name="Swagger Generator",
    role="Generates OpenAPI 3.0 YAML",
    goal="Generate a comprehensive Swagger file from extracted PRD features.",
    backstory=(
        "A seasoned API developer with expertise in translating product requirements into OpenAPI specifications. "
        "Skilled in mapping features to RESTful API endpoints, defining parameters, request/response data models, "
        "and ensuring the Swagger documentation is correct. The goal is to generate a complete, detailed API specification."
    ),
    model="gpt-4-turbo",
    api_key=OPENAI_API_KEY,
    verbose=True,
    constraints=[
        "Dynamically extract all API endpoints, methods (GET, POST, PUT, DELETE), and request/response data models from the processed PRD.",
        "Ensure the Swagger YAML follows OpenAPI 3.0 standards.",
        "Include authentication and authorization details (OAuth 2.0, API Key, etc.) where applicable.",
        "Ensure that all features under the 'API Specification' section are properly documented, including edge cases and error responses.",
        "Verify that the generated Swagger file is well-structured and includes all required API metadata (e.g., title, description, version).",
        "Ensure that all RESTful API paths are fully defined with complete details for each endpoint, including sample requests, responses, and status codes.",
        "The Swagger YAML should include detailed request/response models, including properties, data types, validation rules, and example data.",
        "Ensure comprehensive documentation for each API, including query parameters, headers, body parameters, status codes (200, 400, 500), and potential error messages."
    ],
    expected_output="A fully structured and detailed Swagger YAML file that includes every API endpoint, all necessary details, authentication, and error handling."
)

# Validation Agent
validation_agent = Agent(
    name="Swagger Validation Agent",
    role="Validates generated Swagger (OpenAPI) YAML file.",
    goal="Validate the Swagger YAML file against OpenAPI 3.0 standards, ensuring it adheres to required structure, data types, and security standards.",
    backstory=(
        "A highly skilled API architect with a deep understanding of OpenAPI 3.0 standards and API validation. "
        "Experienced in ensuring that API documentation meets all specifications and provides clear, consistent, and accurate information to developers and consumers."
    ),
    model="gpt-4-turbo",  # Can use GPT-3.5 or GPT-4 models for validation tasks
    api_key=OPENAI_API_KEY,
    verbose=True,
    constraints=[
        "Ensure the Swagger YAML follows OpenAPI 3.0 standards.",
        "Validate that all paths, methods, and response codes are correctly defined and match the API requirements.",
        "Check for consistency and completeness in request/response models, including properties, data types, and validation rules.",
        "Ensure that all authentication and authorization details (OAuth, API Key, etc.) are correctly included.",
        "Verify that error responses are properly documented with status codes (400, 404, 500) and example messages.",
        "Ensure the Swagger file includes metadata such as title, version, description, and contact info.",
    ],
    expected_output="A validated and error-free Swagger YAML file, fully compliant with OpenAPI 3.0 standards."
)
