import openai
import os
import time
import re
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
client = openai.Client(api_key=OPENAI_API_KEY)


def extract_score_from_text(text):
    patterns = [
        r"\bscore\b[:=]?\s*([0-1](?:\.\d+)?)",                         
        r"\bscore.*?\b([0-1](?:\.\d+)?)",                              
        r"\b(?:rated|rates?|rate it|give it)\b.*?\b([0-1](?:\.\d+)?)", 
        r"\b([0-1](?:\.\d+)?)\b\s*(?:out of|/)\s*1",                   
        r"\b([0-1](?:\.\d+)?)\b"                                       
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                value = float(match.group(1))
                if 0 <= value <= 1:
                    return value
            except:
                continue

    print(f"Could not parse entailment score from: {text}")
    return 0.0


def extract_api_spec_section(prd_text):
    """Extract only the 'API Specification' section from the PRD."""
    match = re.search(r"(?i)###?\s*API Specification\s*(.*?)\s*(###|$)", prd_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    print("Could not find 'API Specification' section in PRD.")
    return prd_text  # fallback to full PRD if section missing


def summarize(text, label):
    """Summarize either PRD or Swagger in functional terms."""
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior API analyst. Summarize the key functional behaviors described in the input. "
                    "Avoid technical jargon, and instead describe what the system does from a business logic/API perspective."
                )
            },
            {
                "role": "user",
                "content": f"{label}:\n{text}"
            }
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()


def generate_explanations(prd, swagger_yaml, n=5):
    explanations = []
    for _ in range(n):
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert analyst tasked with verifying whether an API specification "
                        "implements the behavior described in a product requirements document (PRD). "
                        "Focus on the functionality — like endpoints, actions, and data structures — without referencing Swagger, YAML, or OpenAPI. "
                        "Your explanation should describe whether and how the implementation fulfills the PRD's functional goals."
                    )
                },
                {
                    "role": "user",
                    "content": f"""PRD:
{prd}

API Implementation:
{swagger_yaml}

Explain how the API implementation satisfies the PRD's functional requirements."""
                }
            ],
            temperature=0.2
        )
        explanation = response.choices[0].message.content.strip()
        explanations.append(explanation)
        time.sleep(1)  # avoid rate limit
    return explanations


def compute_entailment(text_a, text_b):
    """Measure entailment between two functional summaries."""
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a reasoning engine. Given two summaries, rate how well the second logically implements the first. Score from 0 (not entailed) to 1 (fully entailed)."
            },
            {
                "role": "user",
                "content": f"""
Summary A (PRD):
{text_a}

Summary B (Swagger):
{text_b}

Score the degree to which Summary B faithfully implements Summary A."""
            }
        ],
        temperature=0.2
    )
    score_text = response.choices[0].message.content.strip()
    try:
        return extract_score_from_text(score_text)
    except:
        print(f"Could not parse entailment score from: {score_text}")
        return 0.0


def compute_similarity_score(text_a, text_b):
    """Returns a similarity ratio between two Swagger YAMLs or large texts (0 to 1)."""
    return SequenceMatcher(None, text_a, text_b).ratio()


def evaluate_stable_confidence(prd, swagger_yaml, n=3):
    """Compute confidence and stability by comparing functional summaries."""
    summaries = []
    entailments = []

    # Focus only on the 'API Specification' section of PRD
    api_spec_text = extract_api_spec_section(prd)

    # Summarize that focused API Specification content
    print(f"\nExtracted 'API Specification' section:\n{api_spec_text}\n")
    prd_summary = summarize(api_spec_text, "PRD - API Specification")
    print(f"\nPRD Functional Summary:\n{prd_summary}\n")

    # Loop to check consistency of entailment scoring
    for i in range(n):
        swagger_summary = summarize(swagger_yaml, "Swagger YAML")
        summaries.append(swagger_summary)
        score = compute_entailment(prd_summary, swagger_summary)
        entailments.append(score)
        time.sleep(1)

    confidence_score = sum(entailments) / len(entailments)
    stability_score = 1 - (max(entailments) - min(entailments))  # Variance-based

    return {
        "confidence_score": round(confidence_score, 3),
        "stability_score": round(stability_score, 3),
        "entailment_scores": entailments,
        "swagger_summaries": summaries,
        "prd_summary": prd_summary
    }
