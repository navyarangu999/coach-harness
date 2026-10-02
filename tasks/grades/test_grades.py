from grades import percentage


def test_percentage():
    assert percentage(1, 8) == 12.5


def test_percentage_half():
    assert percentage(1, 2) == 50.0
