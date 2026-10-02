from product import product


def test_product():
    assert product([2, 3, 4]) == 24


def test_product_single():
    assert product([7]) == 7
