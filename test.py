with open("words_alpha.txt") as f:
    word_set = set(word.strip().lower() for word in f)

def word_exists(word):
    return word.lower() in word_set

# Test
print(word_exists("hello"))  # True
print(word_exists("asdf"))   # False