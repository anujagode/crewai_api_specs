from crewai import Task

def self_eval_task(agent, prd_text, swagger_yaml):
    return Task(
        description=f"""
        :pushpin: **Evaluate Swagger YAML for completeness and alignment with PRD:**

        --- PRD ---
        {prd_text}
        --- END PRD ---

        --- SWAGGER YAML ---
        {swagger_yaml}
        --- END SWAGGER YAML ---

        Return a single confidence score between 0.0 and 1.0 representing how well the Swagger matches the PRD.
        """,
        agent=agent,
        expected_output="Confidence score as a float (e.g., 0.88)"
    )
