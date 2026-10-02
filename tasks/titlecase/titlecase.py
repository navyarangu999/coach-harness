def capitalize_words(sentence):
    """Capitalize the first letter of each word."""
    return " ".join(word.capitalize() for word in sentence.split(" "))
