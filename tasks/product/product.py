def product(numbers):
    """Return the product of all numbers in a list."""
    result = 1
    for n in numbers:
        result *= n
    return result
