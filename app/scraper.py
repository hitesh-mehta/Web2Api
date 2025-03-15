import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Scraper for static websites
def scrape_static_website(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return {"error": f"Failed to fetch URL, status code: {response.status_code}"}

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else "No title found"
    links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
    return {"title": title, "links": links}

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def scrape_dynamic_website(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Use installed Chrome binary
    chrome_options.binary_location = "/usr/bin/google-chrome"

    # Use installed Chromedriver
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    return {"html": page_source}
