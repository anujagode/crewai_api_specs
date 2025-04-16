from crewai import Crew
from agents.swagger_generator_agent import swagger_generator_agent
from agents.validation_agent import validation_agent
from agents.self_eval_agent import self_eval_agent
from tasks.generate_swagger_task import generate_swagger_task
from tasks.validate_swagger_task import validate_swagger_task
from tasks.self_eval_task import self_eval_task

class SwaggerCrew:
    def create_prd_processing_crew(self, extracted_text):
        """Creates a crew to process PRD and generate Swagger YAML."""
        
        if not extracted_text or not extracted_text.strip():
            raise ValueError("Error: PRD text is empty or missing!")

        swagger_agent = swagger_generator_agent(extracted_text)
        print(swagger_agent)
        
        swagger_task = generate_swagger_task(swagger_agent, extracted_text)  

        prd_crew = Crew(
            agents=[swagger_agent],
            tasks=[swagger_task],
            verbose=True
        )

        print("PRD Processing Crew Initialized Successfully")
        return prd_crew

    def create_validation_crew(self, extracted_text, swagger_yaml):
        """Creates a crew responsible for validating Swagger YAML."""
        
        if not swagger_yaml or not swagger_yaml.strip():
            raise ValueError("Error: Swagger YAML content is missing!")

        validation_agent_instance = validation_agent(extracted_text, swagger_yaml)  
        validation_task = validate_swagger_task(validation_agent_instance, extracted_text, swagger_yaml)  

        validation_crew = Crew(
            agents=[validation_agent_instance],
            tasks=[validation_task],
            verbose=True
        )

        print("Validation Crew Initialized Successfully")
        return validation_crew
    
    def create_self_eval_crew(self, extracted_text, swagger_yaml):
        eval_agent = self_eval_agent(extracted_text, swagger_yaml)
        eval_task = self_eval_task(eval_agent, extracted_text, swagger_yaml)

        eval_crew = Crew(
            agents=[eval_agent],
            tasks=[eval_task],
            verbose=True
        )

        print("Self-Evaluation Crew Initialized Successfully")
        return eval_crew
