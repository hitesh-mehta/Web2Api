import google.generativeai as genai
from config import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

def generate_api_structure(scraped_data):
    prompt = f"""
    Given the following website data, generate a structured REST API with relevant endpoints:
    {scraped_data}

    Provide:
    - Endpoint names
    - HTTP methods (GET/POST)
    - JSON responses
    Do not give any documentation here as I'll get that separately.
    Properly structure the API for a RESTful design. Do not use any formatting.
    """

    response = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)
    return response.text
