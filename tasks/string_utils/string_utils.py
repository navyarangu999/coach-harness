def reverse_words(sentence):
    """Reverse the order of words in a sentence.
    'hello world foo' -> 'foo world hello'
    """
    words = sentence.split(" ")
    return " ".join(reversed(words))


def count_vowels(text):
    """Count the vowels in a string."""
    return sum(1 for ch in text.lower() if ch in "aeiou")