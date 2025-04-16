from crewai import Task

def validate_swagger_task(agent,extracted_text, swagger_yaml):
    """Create the task for validating Swagger YAML."""
    return Task(
        description=f""" 
        :pushpin: **Validate Swagger YAML against PRD and OpenAPI 3.0.3 standards:**

        --- PRD CONTENT ---
        {extracted_text}
        --- END PRD CONTENT ---

        --- SWAGGER YAML CONTENT ---
        {swagger_yaml}
        --- END SWAGGER YAML ---

        :small_blue_diamond: **Validation Focus:**
          - Swagger structure: paths, responses, schemas, metadata.
          - PRD coverage: All described endpoints and behaviors must be present.
          - Ensure each API's methods, models, and responses match PRD requirements.
        """,
        agent=agent,
        expected_output=""" 
        :white_check_mark: **Validation Results:**
        - Swagger is OpenAPI 3.0.3 compliant.
        - All PRD APIs are covered with correct methods and schemas.
        - Any issues or mismatches are listed.
        """
    )
