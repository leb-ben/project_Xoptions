import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from utilities import normalize_url

def get_sub_domains_and_directories(url):
    links = set()
    with Progress() as progress:
        task = progress.add_task("[cyan]Scraping...", total=80)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(url, href)
            if full_url.startswith(url) and len(links) < 80:
                links.add(full_url)
                progress.update(task, advance=1)
    return list(links)

def process_option5(urls):
    console = Console()
    table = Table(title="Scrapped URL List")
    table.add_column("Scrapped URL #", style="cyan", justify="left")
    table.add_column("URL", style="blue", no_wrap=True)
    table.add_column("Source_URL", justify="right", style="green", no_wrap=True)

    for url in urls:
        normalized_url = normalize_url(url)
        sub_domains_and_directories = get_sub_domains_and_directories(normalized_url)
        for i, sub_url in enumerate(sub_domains_and_directories, 1):
            table.add_row(str(i), sub_url, f"from input_url: {normalized_url}")

    console.print(table)
