#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress
from rich import print
from time import sleep
import threading
import colorful
from utilities import normalize_url, print_colored
from blinking_title import print_blinking_title
from option2 import process_option2
from option3 import process_option3
from option4 import process_option4
from option5 import process_option5

def get_hex_strings(html):
    return '\n'.join(re.findall(r'[A-Fa-f0-9]{64}', html))

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
                        hex_strings = get_hex_strings(html)
                        if hex_strings:
                            print_colored(hex_strings)
                        else:
                            print(f"No hex strings found in {normalized_url}")
                    elif option == 2:
                        process_option2(html)
                    elif option == 3:
                        process_option3(html)
                    elif option == 4:
                        process_option4(html)
                    elif option == 5:
                        process_option5(normalized_url)
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
