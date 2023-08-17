import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from rich import print
from rich.color import Color
from rich.style import Style
import colorful

def print_colored(text, gradient=None):
    if gradient:
        colors = ["red", "orange", "yellow", "green", "blue", "cyan", "violet"]
        gradient_text = ""
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            gradient_text += getattr(colorful, color)(char)
        print(gradient_text)
    else:
        print(text)

unique_values = set()

def normalize_url(url, fallback_scheme='http'):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme or 'https'
    netloc = parsed_url.netloc or parsed_url.path
    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc
    if not scheme:
        scheme = 'https'
    normalized_url = scheme + '://' + netloc

    # You can add logic here to attempt to fetch the content using the normalized URL
    # and then fall back to the fallback_scheme if needed.

    return normalized_url


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
