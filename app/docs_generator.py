def generate_openapi_doc(api_structure):
    prompt = f"Generate API documentation for the following API structure:\n{api_structure} Be as detailed as possible."
    
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text  # AI-generated documentation
