"""StudyTools 1.0: fictional, dependency-free teaching API, not a PyPI package."""
__version__ = '1.0'


def take(items, limit=2):
    if type(limit) is not int:
        raise TypeError('limit must be an integer, not bool')
    if limit < 0:
        raise ValueError('limit must be nonnegative')
    return items[:limit].copy()


def find(items, target, default=None):
    for index, item in enumerate(items):
        if item == target:
            return index
    return default


def clip(x, low=0, high=10):
    if low > high:
        raise ValueError('low must not exceed high')
    return min(max(x, low), high)
