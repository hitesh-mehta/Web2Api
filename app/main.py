from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.scraper import scrape_static_website, scrape_dynamic_website
from app.ai_processor import generate_api_structure
from app.docs_generator import generate_openapi_doc
import os
# Allow CORS from all domains (for testing) or restrict to your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with ["https://your-frontend.com"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI()

def is_inadequate(scraped_data):
    if "links" in scraped_data and len(scraped_data.keys()) == 1:
        return True
    return False

@app.get("/generate-api/")
async def generate_api(url: str):
    try:
        if url.endswith(".html"):
            is_dynamic = False
        else:
            is_dynamic = True

        if is_dynamic:
            scraped_data = scrape_dynamic_website(url)  # Selenium
        else:
            static_scraped_data = scrape_static_website(url)  # BeautifulSoup
            if is_inadequate(static_scraped_data):
                scraped_data = scrape_dynamic_website(url)  # Selenium
            else:
                scraped_data = static_scraped_data

        api = generate_api_structure(scraped_data)
        documentation = generate_openapi_doc(api)
        return {"success": True, "api": api,"documentation":documentation}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# 🚀 Run on an empty port dynamically assigned by Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT not found
    uvicorn.run(app, host="0.0.0.0", port=port)