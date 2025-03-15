def generate_openapi_doc(api_structure):
    prompt = f"Generate OpenAPI 3.0 documentation for the following API structure:\n{api_structure}"
    
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text  # AI-generated documentation
