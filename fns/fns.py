import json
import pickle
from collections import Counter
import os
from more_itertools import flatten

from fns.text import md5_hash


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


def percent_dict(key_value):
    total = sum(key_value.values())
    return {key: value / total * 100.0 for key, value in key_value.items()}


def top(data, n=5):
    return dict(Counter(data).most_common(n))


def top_n_from_dict(dictionary, n: int = 10):
    """
    Get top n largest values from the dictionary.
    :param dictionary: Python dictionary
    :param n: Number of keys to pick
    """
    return top(dictionary, n=n)


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


def parse_manual(parser, command):
    """
    Use argument parser in notebooks.

    :param parser: ArgumentParser
    :param command: Command line arguments as string
    :return: Parserd argument as namespace
    """
    args = command.split()
    return parser.parse_args(args=args)


def hash_file(file_object):
    """
    Calculate hash of file.
    :param file: File object
    :return: MD5 hash of the file
    """
    # Calculate hash
    unique_hash = md5_hash(file_object.read())

    # Reset file pointer to start
    file_object.seek(0)

    return unique_hash


def num_files(path):
    return len(os.listdir(path))
