import re
import requests
from utilities import normalize_url, print_colored
from rich.progress import Progress

def get_hex_strings(html):
    return '\n'.join(re.findall(r'[A-Fa-f0-9]{64}', html))
    
def process_option1(urls, headers):
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing...", total=len(urls))
        for url in urls:
            normalized_url = normalize_url(url)
            try:
                response = requests.get(normalized_url, headers=headers, timeout=10)  # 10-second timeout
                html = response.text
                hex_strings = get_hex_strings(html)
                if hex_strings:
                    print_colored(hex_strings)
                else:
                    print(f"No hex strings found in {normalized_url}")
            except requests.exceptions.Timeout:
                print(f"Timed out while processing {normalized_url}. Moving on to the next URL.")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while processing {normalized_url}: {e}. Moving on to the next URL.")
            progress.update(task, advance=1)
