import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver

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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        data = driver.page_source
        driver.quit()

        return {"html": data}

    except Exception as e:
        return {"error": f"Chrome failed: {str(e)}"}
