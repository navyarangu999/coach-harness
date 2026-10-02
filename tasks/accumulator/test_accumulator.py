from accumulator import add_item


def test_fresh_basket_each_call():
    assert add_item("a") == ["a"]
    assert add_item("b") == ["b"]
