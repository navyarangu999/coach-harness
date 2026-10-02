from titlecase import capitalize_words


def test_capitalize_words():
    assert capitalize_words("hello there world") == "Hello There World"
