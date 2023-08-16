from urllib.parse import urlparse
import colorful

def normalize_url(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme or 'http'
    netloc = parsed_url.netloc or parsed_url.path
    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc
    return scheme + '://' + netloc

def print_colored(text, gradient=None):
    import colorful
    if gradient:
        colors = ["red", "orange", "yellow", "green", "blue", "cyan", "violet"]
        gradient_text = ""
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            gradient_text += getattr(colorful, color)(char)
        print(gradient_text)
    else:
        print(text)
