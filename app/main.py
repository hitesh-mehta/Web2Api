from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.scraper import scrape_static_website, scrape_dynamic_website
from app.ai_processor import generate_api_structure
import os

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

        ai_generated_api = generate_api_structure(scraped_data)
        return {"success": True, "api": ai_generated_api}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# 🚀 Run on an empty port dynamically assigned by Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT not found
    uvicorn.run(app, host="0.0.0.0", port=port)