def last_n(items, n):
    """Return the last n items of a list, in order."""
    if n <= 0:
        return []
    return items[-n:]
