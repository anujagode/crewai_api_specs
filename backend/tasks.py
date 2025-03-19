from crewai import Task
from agents import swagger_generator_agent, validation_agent

# Task to generate Swagger YAML from processed PRD text
generate_swagger_task = Task(
    description=""" 
    :pushpin: **Generate OpenAPI 3.0 YAML from Processed PRD Text.**
    :small_blue_diamond: **PRD Text Analysis:**
      - Extract relevant API endpoints, methods (GET, POST, PUT, DELETE), and data structures from the processed PRD.
      - Identify key resources (e.g., user, connection, application) and their relationships.
      - Map functionality to RESTful API endpoints (GET, POST, PUT, DELETE).

    :small_blue_diamond: **Swagger YAML Generation:**
      - Generate a valid OpenAPI 3.0 YAML specification based on the extracted PRD features.
      - Include metadata such as API version, title, and description.
      - Structure the endpoints with required HTTP methods (GET, POST, PUT, DELETE).
      - Ensure API versioning is properly defined in the Swagger metadata.

    :small_blue_diamond: **Schema & Response Definition:**
      - Define request and response schemas for each API endpoint using JSON Schema format.
      - Include necessary status codes and response models (e.g., 200, 400, 404, 500).
      - Ensure proper data types, constraints, and validation for API inputs and outputs.

    :small_blue_diamond: **Security & Compliance:**
      - Include authentication mechanisms (e.g., OAuth 2.0, API Key).
      - Ensure compliance with security standards (e.g., HTTPS, CORS).
      - Define required permissions and roles for accessing specific API endpoints.

    :small_blue_diamond: **Documentation & Testing:**
      - Ensure that the generated API documentation is comprehensive and user-friendly.
      - Provide examples for request and response bodies, query parameters, and error handling.
      - Generate sample API calls and expected responses.
    """,
    agent=swagger_generator_agent,
    expected_output=""" 
    :white_check_mark: **Generated Swagger YAML Includes:**
    - Complete OpenAPI 3.0 specification for the product API.
    - Valid endpoint definitions, including HTTP methods and parameters.
    - Request and response schemas with example data.
    - Security and authentication details (OAuth, API Key, etc.).
    - Documentation for API usage, error handling, and testing.
    - Sample API requests and responses with expected status codes.
    """
)

# Task to validate Swagger YAML against OpenAPI 3.0 standards
validate_swagger_task = Task(
    description=""" 
    :pushpin: **Validate Swagger YAML (OpenAPI 3.0) Format.**
    :small_blue_diamond: **Swagger YAML Validation:**
      - Validate that the Swagger YAML follows OpenAPI 3.0 standards.
      - Check for correct structure, data types, response codes, and paths.
      - Ensure authentication (OAuth, API Key) is correctly defined.
      - Ensure that response models, status codes, and error handling are properly documented.
    """,
    agent=validation_agent,
    expected_output=""" 
    :white_check_mark: **Validated Swagger YAML Includes:**
    - Correctly formatted OpenAPI 3.0 YAML.
    - Proper validation of API paths, methods, and response models.
    - Authentication and error handling details.
    - Comprehensive documentation for API usage.
    """
)