import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Scraper for static websites
def scrape_static_website(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch URL: {str(e)}"}

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else "No title found"
    links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
    
    return {"title": title, "links": links}


# Scraper for dynamic websites using Selenium
def scrape_dynamic_website(url: str):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Required for Render
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues
    chrome_options.add_argument("--remote-debugging-port=9222")  # Prevent DevTools crash
    chrome_options.add_argument("--disable-gpu")  # Avoid GPU-related crashes
    chrome_options.add_argument("--disable-software-rasterizer")  # More stability
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Explicitly set binary path

    try:
        service = Service("/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(url)
        data = driver.page_source
        driver.quit()

        return {"html": data}

    except Exception as e:
        return {"error": f"Chrome failed: {str(e)}"}
