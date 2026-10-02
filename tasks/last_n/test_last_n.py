from last_n import last_n


def test_last_n():
    assert last_n([1, 2, 3, 4, 5], 2) == [4, 5]


def test_last_n_all():
    assert last_n([1, 2, 3], 3) == [1, 2, 3]
