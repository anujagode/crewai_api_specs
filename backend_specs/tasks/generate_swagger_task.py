from crewai import Task

def generate_swagger_task(agent, extracted_text):
    """Create the task for generating Swagger YAML."""
    description = f"""
    :pushpin: **Generate an OpenAPI 3.0.3 YAML specification from the following PRD:**

    --- EXTRACTED PRD TEXT ---
    {extracted_text}
    --- END OF EXTRACTED PRD TEXT ---

    :small_blue_diamond: **PRD Text Analysis:**
      - Extract relevant API endpoints, methods (GET, POST, PUT, DELETE), and data structures from the processed PRD.
      - Identify key resources (e.g., user, connection, application) and their relationships.
      - Map functionality to RESTful API endpoints (GET, POST, PUT, DELETE).
    
    :small_blue_diamond: **Swagger YAML Generation:**
      - Generate a valid OpenAPI 3.0.3 YAML specification based on the extracted PRD features.
      - Include metadata such as API version, title, and description.
      - Structure the endpoints with required HTTP methods (GET, POST, PUT, DELETE).
    
    :small_blue_diamond: **Schema & Response Definition:**
      - Define request and response schemas for each API endpoint using JSON Schema format.
      - Include necessary status codes and response models (e.g., 200, 400, 404, 500).
    """

    return Task(
        description=description,  
        agent=agent,
        expected_output=""" 
        :white_check_mark: **Generated Swagger YAML Includes:**
        - Complete OpenAPI 3.0.3 specification for the product API.
        - Valid endpoint definitions, including HTTP methods and parameters.
        - Request and response schemas with example data.
        - Do not add security and authentication details (OAuth, API Key, etc.).
        """
    )
