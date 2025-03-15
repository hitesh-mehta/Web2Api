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

def scrape_dynamic_website(url):
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"  # Explicitly set Chrome binary path
    service = Service("/usr/local/bin/chromedriver")  # Use installed ChromeDriver

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    data = driver.page_source
    driver.quit()
    return {"html": data}
