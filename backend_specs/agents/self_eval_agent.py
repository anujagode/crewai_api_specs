from crewai import Agent
import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def self_eval_agent(prd_text, swagger_yaml):
    prompt = f"""
You are a self-evaluation agent designed to assess how well a Swagger YAML file covers the requirements in a PRD.

--- PRD START ---
{prd_text}
--- PRD END ---

--- SWAGGER YAML START ---
{swagger_yaml}
--- SWAGGER YAML END ---

Evaluate how completely and accurately the Swagger YAML captures the APIs, methods, models, and structure from the PRD. Consider:
- PRD coverage
- Accuracy of endpoints and methods
- Correct use of request/response schemas
- OpenAPI structure quality

Respond ONLY with a confidence score between 0.0 (very poor) and 1.0 (perfect). No explanation.
"""

    return Agent(
        name="Self-Eval Agent",
        role="Self-assesses coverage of Swagger YAML vs PRD",
        goal="Return a numerical confidence score (0.0 - 1.0) representing Swagger YAML accuracy and completeness.",
        backstory="An expert QA agent designed to evaluate documentation accuracy using internal model awareness.",
        model="gpt-4-turbo",
        api_key=OPENAI_API_KEY,
        temperature=0.2,
        context=prompt,
        verbose=True,
        constraints=[
            "Output only a number between 0.0 and 1.0.",
            "Do not include explanations, comments, or markdown.",
        ],
        expected_output="Float score from 0.0 to 1.0 indicating confidence in the Swagger YAML's accuracy."
    )
