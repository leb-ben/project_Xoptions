from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
from rich.table import Table
from rich.console import Console
import requests

KEYWORDS = ['privKey', 'seed', 'key', 'mnemonic', 'p2p', 'asset', 'address', 'wallet', 'access', 'crypto', 'eth', 'erc20']

def process_option5(url):
    print(f"Processing URL: {url}")
    console = Console()
    table_title = f"Scrapped URL List from input_url: {url}"
    table = Table(title=table_title)
    table.add_column("Scrapped URL #", style="cyan", justify="left")
    table.add_column("URL", no_wrap=False)
    table.add_column("Source_URL", justify="right", style="green", no_wrap=True)

    links = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(url, href)
            if full_url.startswith(url) and len(links) < 50:
                if any(keyword.lower() in full_url.lower() for keyword in KEYWORDS):
                    print(f"Keyword found: {keyword}")
                    links.add(full_url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing {url} with BeautifulSoup: {e}")

    if len(links) >= 50:
        try:
            driver = webdriver.Chrome(executable_path='chromedriver.exe')
            driver.get(url)
            a_tags = driver.find_elements(By.TAG_NAME, 'a')
            for a in a_tags:
                href = a.get_attribute('href')
                if href and href.startswith(url) and len(links) < 70:
                    if any(keyword.lower() in href.lower() for keyword in KEYWORDS) and href not in links:
                        links.add(href)
            driver.quit()
        except Exception as e:
            print(f"An error occurred while processing {url} with Selenium: {e}")

    for i, sub_url in enumerate(links, 1):
        table.add_row(str(i), sub_url, f"[cyan]from input_url: {url}")

    console.print(table)
