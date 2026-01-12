def generator_example(n):
    """
    Generate a sequence

    Args:
        n (TYPE): number of elements to generate

    Returns:
        TYPE: a sequence of numbers
    """
    for i in range(n):
        yield i

def raises_example(x):
    if x < 0:
        raise ValueError("Negative")
    return x * 2

