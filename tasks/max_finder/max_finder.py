def find_max(numbers):
    """Return the largest number in a non-empty list."""
    best = numbers[0]
    for n in numbers:
        if n > best:
            best = n
    return best
