import heapq
import json
import pickle

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


def reverse_mapping(dictionary):
    """
    Swap mapping from key: value to value:key
    :param dictionary: Python Dictionary
    :return: Dictionary with key and value swapped
    """
    return {v: k for k, v in dictionary.items()}


def top_n_from_dict(dictionary, n: int = 10):
    """
    Get top n largest values from the dictionary.
    :param dictionary: Python dictionary
    :param n: Number of keys to pick
    """
    return dict(heapq.nlargest(n, dictionary.items(), key=lambda item: item[1]))


def read_json(json_path):
    """
    Read json file from a path.
    """
    with open(json_path, 'r') as fp:
        data = json.load(fp)
    return data


def write_json(item, path, mode='w'):
    """
    Save json to a file.
    """

    with open(path, mode=mode) as fp:
        json.dump(item, fp)


def read_pickle(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)


def write_pickle(item, path):
    with open(path, 'wb') as fp:
        return pickle.dump(item, fp)
