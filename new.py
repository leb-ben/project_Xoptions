#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich import print
from rich.color import Color
from time import sleep
from rich.style import Style
import threading
import colorful

def print_blinking_title(title, colors, stop_event, blink_rate=0.5):
    console = Console()
    while not stop_event.is_set():
        for color in colors:
            if stop_event.is_set():
                break
            style = Style(color=color)
            console.print(title, style=style)
            sleep(blink_rate)

def process_data():
    sleep(0.02)

def normalize_url(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme or 'http'
    netloc = parsed_url.netloc or parsed_url.path
    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc
    return scheme + '://' + netloc
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
    with Progress() as progress:
        task = progress.add_task("[cyan]Scraping...", total=50)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(url, href)
            if full_url.startswith(url) and len(links) < 50:
                links.add(full_url)
                progress.update(task, advance=1)
    return list(links)

def main():
    while True:  # Outer loop to restart the script
        urls = [url.strip() for url in input("Please enter a URL or a list of URLs separated by commas: ").split(',')]

        while True:  # Inner loop for selecting options
            prompt_text = "Choose an option to crawl/scrape the given URL(s) for:\n" \
                          "[1]: any 64 char hex strings\n" \
                          "[2]: Any login credentials\n" \
                          "[3]: Any Variables (or hard coded) where the name included the word 'key' in some part of it\n" \
                          "[4]: Return entire line if this word appears [user input]\n" \
                          "[5]: a list of up to 50 sub domains / directories / unique pages that begin with the given URL\n"
            
            colors = ["red", "orange", "yellow", "green", "blue", "cyan", "violet"]
            gradient_prompt_text = ""
            lines = prompt_text.split("\n")
            for i, line in enumerate(lines):
                color = colors[i % len(colors)]
                gradient_prompt_text += getattr(colorful, color)(line) + "\n"

            option = int(input(gradient_prompt_text))

            headers = {'User-Agent': 'Mozilla/5.0'}  # Add a User-Agent header

            try:
                for url in urls:
                    normalized_url = normalize_url(url)
                    try:
                        response = requests.get(normalized_url, headers=headers)  # Include the headers in the request
                        html = response.text
                    except requests.exceptions.RequestException as e:
                        print(f"An error occurred while processing {normalized_url}: {e}")
                        continue  # Skip to the next URL
            
                    if option == 1:
                        colorful.use_style('solarized')
                        print_colored(get_hex_strings(html))
                    elif option == 2:
                        colorful.use_style('solarized')
                        print_colored(get_login_credentials(html))
                    elif option == 3:
                        colorful.use_style('solarized')
                        print_colored(get_key_variables(html))
                    elif option == 4:
                        colorful.use_style('solarized')
                        word = input("Please enter the keyword or phrase to use: ")
                        print_colored(get_lines_with_word(html, word))
                    elif option == 5:
                        stop_event = threading.Event()
                        blink_colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
                        blink_thread = threading.Thread(target=print_blinking_title, args=("Scrapped URL List", blink_colors, stop_event))
                        blink_thread.start()
                        console = Console()
                        table_title = f"Scrapped URL List from input_url: {normalized_url}"
                        table = Table(title=table_title)
                        table.add_column("Scrapped URL #", style="cyan", justify="left")
                        table.add_column("URL", style="blue", no_wrap=True)
                        table.add_column("Source_URL", justify="right", style="green", no_wrap=True)
                    
                        for url in urls:
                            normalized_url = normalize_url(url)
                            sub_domains_and_directories = get_sub_domains_and_directories(normalized_url)
                            for i, sub_url in enumerate(sub_domains_and_directories, 1):
                                table.add_row(str(i), sub_url, f"from input_url: {normalized_url}")
                    
                        console.print(table)
                    
                    else:
                        print("Invalid option")

                break  # Break the inner loop if no errors occurred

            except Exception as e:
                print(f"An error occurred: {e}. Please try again.")

        # Options to restart the script
        restart_option = input("Choose an option:\n[1]: Start from the beginning\n[2]: Start with the URLs from option [5]\n")
        if restart_option == '1':
            continue
        elif restart_option == '2':
            urls = get_sub_domains_and_directories(normalized_url)  # Assuming you want to use the last URL processed
            continue
        else:
            print("Invalid option. Starting from the beginning.")


if __name__ == "__main__":
    main()
