from math_utils import average, is_even


def test_average():
    assert average([1, 2, 4]) == 2.3333333333333335


def test_is_even():
    assert is_even(4) is True
    assert is_even(7) is False