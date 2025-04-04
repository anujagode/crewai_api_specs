from crewai import Task

def validate_swagger_task(agent,swagger_yaml):
    """Create the task for validating Swagger YAML."""
    return Task(
        description=""" 
        :pushpin: **Validate OpenAPI 3.0.3 YAML specification from the following swagger_yaml:\n\n{swagger_yaml}.**
        :small_blue_diamond: **Swagger YAML Validation:**
          - Validate that the Swagger YAML follows OpenAPI 3.0.3 standards.
          - Check for correct structure, data types, response codes, and paths.
          - Ensure authentication (OAuth, API Key) is correctly defined.
        """,
        agent=agent,
        expected_output=""" 
        :white_check_mark: **Validated Swagger YAML Includes:**
        - Correctly formatted OpenAPI 3.0.3 YAML.
        - Proper validation of API paths, methods, and response models.
        """
    )
