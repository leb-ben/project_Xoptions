import argparse
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlencode, urlparse, parse_qs


class MySpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self, url=None, query=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [url + '/?' + urlencode({'q': query})]
        self.query = query
        self.hex_strings = []

    def parse(self, response):
        # Extract the search results link from the page
        search_url = response.css('a::attr(href)').re_first(r'/search\?[^"]+')

        if search_url:
            # Parse the search results link
            search_url = response.urljoin(search_url)
            search_query = parse_qs(urlparse(search_url).query)

            # Get the URLs of the search results pages
            for page_num in range(1, 6):
                search_query['start'] = str((page_num - 1) * 10)
                search_url_page = search_url.split('&')[0] + '&' + urlencode(search_query)
                yield scrapy.Request(url=search_url_page, callback=self.parse_results_page)

    def parse_results_page(self, response):
        # Extract the URLs from the search results page
        for href in response.css('a::attr(href)').extract():
            if href.startswith('/url?q='):
                url = href.split('=')[1].split('&')[0]
                yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        # Extract the hex strings from the page
        for hex_str in response.css('body ::text').re(r'[a-f0-9]{64}'):
            # Check if the hex string meets additional search parameters
            if hex_str != "0000000000000000000000000000000000000000000000000000000000000000":
                # Check if the page contains all 3 words
                if all(word.lower() in response.text.lower() for word in self.query.split()):
                    self.hex_strings.append(hex_str)

    def closed(self, reason):
        # Print the hex strings found to the console
        print('\n'.join(self.hex_strings))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Crawl a website and search for hex strings that meet certain search parameters.")
    parser.add_argument("url", type=str, help="the URL of the website")
    parser.add_argument("--query", type=str, help="the search query to use")
    args = parser.parse_args()

    if args.query is None:
        query = input("Enter the search query: ")
    else:
        query = args.query

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        # Set the maximum number of simultaneous requests (optional)
        'CONCURRENT_REQUESTS': 16,
        # Set the maximum depth of the crawling (optional)
        'DEPTH_LIMIT': 250,
        # Set the maximum length of time (in secs) that the spider will run until termination (optional)
        'CLOSESPIDER_TIMEOUT': 36000,
        # Set the maximum number of redirects allowed (optional)
        'HTTPERROR_ALLOW_ALL': True,
        # Enable cookies (optional)
        'COOKIES_ENABLED': False,
    })

    process.crawl(MySpider, url=args.url, query=query)
    process.start()