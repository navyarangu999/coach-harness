from countdown import countdown


def test_countdown():
    assert countdown(5) == [5, 4, 3, 2, 1]


def test_countdown_one():
    assert countdown(1) == [1]
