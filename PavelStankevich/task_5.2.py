# Task 5.2
import re

def most_common_word(filepath, number_of_words=3):
    """Return a list of the most common words in the file."""
    with open(filepath) as file:
        word_dict = dict()
        text = file.read()

    word_list = re.findall(r"\w+\b", text.lower())

    for word in word_list:
        word_dict[word] = word_list.count(word)

    return [word for word, count in sorted(word_dict.items(), key=lambda item: item[1], reverse=True)][:number_of_words]

print(most_common_word("data/lorem_ipsum.txt", 5))
