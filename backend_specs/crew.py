from crewai import Crew
from agents.swagger_generator_agent import swagger_generator_agent
from agents.validation_agent import validation_agent
from tasks.generate_swagger_task import generate_swagger_task
from tasks.validate_swagger_task import validate_swagger_task

class SwaggerCrew:
    def create_prd_processing_crew(self, extracted_text):
        """Creates a crew to process PRD and generate Swagger YAML."""
        
        if not extracted_text or not extracted_text.strip():
            raise ValueError("❌ Error: PRD text is empty or missing!")

        swagger_agent = swagger_generator_agent(extracted_text)
        print(swagger_agent)# ✅ Uses extracted API details
        
        swagger_task = generate_swagger_task(swagger_agent, extracted_text)  # ✅ Assigns correct agents

        prd_crew = Crew(
            agents=[swagger_agent],
            tasks=[swagger_task],
            verbose=True
        )

        print("🚀 PRD Processing Crew Initialized Successfully")
        return prd_crew

    def create_validation_crew(self, swagger_yaml):
        """Creates a crew responsible for validating Swagger YAML."""
        
        if not swagger_yaml or not swagger_yaml.strip():
            raise ValueError("❌ Error: Swagger YAML content is missing!")

        validation_agent_instance = validation_agent(swagger_yaml)  # ✅ Properly initializes validation agent
        validation_task = validate_swagger_task(validation_agent_instance, swagger_yaml)  # ✅ Passes Swagger YAML correctly

        validation_crew = Crew(
            agents=[validation_agent_instance],
            tasks=[validation_task],
            verbose=True
        )

        print("✅ Validation Crew Initialized Successfully")
        return validation_crew
