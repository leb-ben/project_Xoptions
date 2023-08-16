import scrapy

class MySpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self, url=None, words=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.words = words.split(" ")

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            # Ensure that the crawler only follows links within the same domain
            if href and self.start_urls[0] in href:
                yield scrapy.Request(url=response.urljoin(href), callback=self.parse_page)

    def parse_page(self, response):
        # Extract the hex strings from the page
        for hex_str in response.css('body ::text').re(r'[a-f0-9]{64}'):
            # Check if the hex string meets additional search parameters
            if hex_str != "0000000000000000000000000000000000000000000000000000000000000000":
                # Check if the page contains all 3 words
                if all(word.lower() in response.text.lower() for word in self.words):
                    yield {"hex_str": hex_str}


if __name__ == '__main__':
    import sys

    url = input("Enter URL to crawl (e.g. https://example.com): ")
    words = input("Enter 3 unique words separated by spaces (e.g. hello world goodbye): ")

    process = scrapy.crawler.CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        # Set the maximum number of simultaneous requests (optional)
        'CONCURRENT_REQUESTS': 16,
        # Set the maximum depth of the crawling (optional)
        'DEPTH_LIMIT': 20,
        # Set the maximum length of time (in secs) that the spider will run until termination (optional)
        'CLOSESPIDER_TIMEOUT': 3600,
        # Set the maximum number of redirects allowed (optional)
        'HTTPERROR_ALLOW_ALL': True,
        # Enable cookies (optional)
        'COOKIES_ENABLED': True,
    })

    process.crawl(MySpider, url=url, words=words)
    process.start()