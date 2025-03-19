import openai
import os
import tiktoken
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.Client(api_key=OPENAI_API_KEY)

# Function to truncate PRD text to fit within model's context limit
def truncate_text_to_tokens(text, max_tokens):
    encoding = tiktoken.encoding_for_model("gpt-4-turbo")  # Choose the correct tokenizer for GPT-4
    tokens = encoding.encode(text)  # Tokenize input text
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]  # Truncate to the allowed limit
    return encoding.decode(tokens)  # Convert back to text

def generate_openai_response(prd_text):
    truncated_text = truncate_text_to_tokens(prd_text, max_tokens=32000)  # Ensure input fits within model limits

    prompt = f"""
    Given the following PRD, generate an OpenAPI 3.0 YAML specification:

    {truncated_text}

    The response should be a complete Swagger YAML file with endpoints, request bodies, response schemas, and authentication details.
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
