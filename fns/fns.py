from itertools import chain
from more_itertools import flatten

def array_except_element(arr, elem):
    """
    Get copy of array without an element.

    >>> array_except_element([1, 2, 3], 3)
    [1, 2]
    """
    elem_index = arr.index(elem)
    return arr[:elem_index] + arr[elem_index + 1:]


def sort_dict_by_value(d, reverse=False):
    """
    Sort items in dictionary by value.
    
    >>> sort_dict_by_value({'gold': 40, 'silver': 25})
    {'silver': 25, 'gold': 40}
    """
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))
