import google.generativeai as genai
from config import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)
def generate_openapi_doc(api_structure):
    prompt = f"""Generate API documentation for the following API structure:
    {api_structure} 
    Be as detailed as possible.
    Reply in plain text without any quotes, code blocks, markdown, or special formatting.
    """
    
    response = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)
    return response.text  # AI-generated documentation
