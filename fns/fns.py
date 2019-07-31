from itertools import chain


def flatten(x):
    return chain.from_iterable(x)


def sort_dict_by_value(d, reverse=False):
    """
    Sort items in dictionary by value.
    
    >>> sort_dict_by_value({'gold': 40, 'silver': 25})
    {'silver': 25, 'gold': 40}
    """
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))
