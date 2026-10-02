from word_count import word_count


def test_simple():
    assert word_count("one two three") == 3


def test_extra_spaces():
    assert word_count("one  two   three") == 3
