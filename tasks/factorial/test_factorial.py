from factorial import factorial


def test_factorial():
    assert factorial(5) == 120


def test_factorial_zero():
    assert factorial(0) == 1
