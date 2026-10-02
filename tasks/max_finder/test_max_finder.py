from max_finder import find_max


def test_find_max():
    assert find_max([3, 7, 2, 9, 4]) == 9


def test_find_max_negatives():
    assert find_max([-5, -2, -9]) == -2
