import itertools
from nltk.corpus import words

# List of letters
letters = ['a', 'b', 'c', 'd', 'e', 'f']

# Get English words
english_words = set(words.words())

# Function to generate words
def generate_words(letters):
    for length in range(1, len(letters) + 1):
        for word_tuple in itertools.product(letters, repeat=length):
            word = ''.join(word_tuple)
            if word in english_words:
                yield word

# Generate words
generated_words = list(generate_words(letters))

# Sort words by length and print the 30 longest
longest_words = sorted(generated_words, key=len, reverse=True)[:30]
for word in longest_words:
    print(word)
