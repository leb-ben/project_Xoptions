from rich.console import Console
from rich.style import Style
from time import sleep

def print_blinking_title(title, colors, blink_rate=1.5):
    console = Console()
    while True:
        for color in colors:
            style = Style(color=color)
            console.print(title, style=style)
            sleep(blink_rate)
