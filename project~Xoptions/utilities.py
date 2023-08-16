import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By

def normalize_url(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme or 'http'
    netloc = parsed_url.netloc or parsed_url.path
    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc
    return scheme + '://' + netloc

def get_hex_strings(html):
    return '\n'.join(re.findall(r'[A-Fa-f0-9]{64}', html))

def get_login_credentials(html):
    users = re.findall(r'u - (.+?)\n', html)
    passwords = re.findall(r'p - (.+?)\n', html)
    return '\n'.join([f'u - {u}\np - {p}' for u, p in zip(users, passwords)])

def get_key_variables(html):
    return '\n'.join(re.findall(r'\b\w*key\w*\b', html, re.IGNORECASE))

def get_lines_with_word(html, word):
    lines = html.split('\n')
    return '\n'.join([line for line in lines if word in line])

def get_sub_domains_and_directories(url):
    links = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(url, href)
            if full_url.startswith(url) and len(links) < 80:
                links.add(full_url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing {url} with BeautifulSoup: {e}")

    if not links:
        try:
            driver = webdriver.Chrome(executable_path='chromedriver.exe')
            driver.get(url)
            a_tags = driver.find_elements(By.TAG_NAME, 'a')
            for a in a_tags:
                href = a.get_attribute('href')
                if href and href.startswith(url) and len(links) < 80:
                    links.add(href)
            driver.quit()
        except Exception as e:
            print(f"An error occurred while processing {url} with Selenium: {e}")

    return list(links)
