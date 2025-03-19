from crewai import Crew
from tasks import generate_swagger_task, validate_swagger_task
from agents import swagger_generator_agent, validation_agent

# Create Crew to handle processing, Swagger generation, and validation
prd_processing_crew = Crew(
    agents=[swagger_generator_agent],  # Include both agents
    tasks=[generate_swagger_task]  # Tasks linked to these agents
)

validation_crew = Crew(
    agents=[validation_agent],  # Include both agents
    tasks=[validate_swagger_task]  # Tasks linked to these agents
)