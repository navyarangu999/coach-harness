def add_item(item, basket=None):
    """Add item to a basket and return it. Each call should start fresh."""
    if basket is None:
        basket = []
    basket.append(item)
    return basket
