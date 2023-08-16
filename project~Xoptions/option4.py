from utilities import print_colored

def get_lines_with_word(html, word):
    lines = html.split('\n')
    return '\n'.join([line for line in lines if word in line])

def process_option4(html):
    word = input("Please enter the keyword or phrase to use: ")
    print_colored(get_lines_with_word(html, word))
