import argparse
import json
import os
import pickle
from argparse import ArgumentParser
from collections import Counter
from itertools import chain
from pathlib import Path
from typing import List, Dict, Union, Iterator, Any, IO

from fns.text import md5_hash


def flatten(x: List[List]) -> Iterator:
    """
    Flatten a list of list.

    Args:
        x: List of list of elements

    Returns:
        Iterator of flattened array.
    """
    return chain.from_iterable(x)


def array_except_element(arr: List, elem: Any) -> List:
    """
    Get copy of array without an element.

    Args:
        arr:
        elem:

    Returns:
        Array

    Example:
    ```python
    >>> array_except_element([1, 2, 3], 3)
    [1, 2]
    ```
    """
    elem_index = arr.index(elem)
    return arr[:elem_index] + arr[elem_index + 1:]


def sort_dict_by_value(d: Dict,
                       reverse: bool = False) -> Dict:
    """
    Sort items in dictionary by value.

    Example:
    ```python
    >>> sort_dict_by_value({'gold': 40, 'silver': 25})
    {'silver': 25, 'gold': 40}
    ```

    Args:
        d: Python Dictionary
        reverse: Sort order

    Returns:
        Sorted dictionary
    """
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))


def reverse_mapping(d: Dict) -> Dict:
    """
    Swap mapping from key: value to value: key

    Args:
        d: Python Dictionary

    Returns:
        Dictionary with key and value swapped
    """
    return {v: k for k, v in d.items()}


def percent_dict(d: Dict) -> Dict:
    """
    Convert a dictionary of key-value to key:coverage-percent.

    Args:
        d: Dictionary of key and values

    Returns:
        Dictionary of key and percent-coverage
    """
    total = sum(d.values())
    return {key: value / total * 100.0
            for key, value in d.items()}


def top(data, n: int = 5) -> Dict:
    """
    Get a dictionary of top-n items from a list.

    Args:
        data: Python collection
        n: Number of top-values

    Returns:
        Dictionary of top-n items and count
    """
    return dict(Counter(data).most_common(n))


def top_n_from_dict(dictionary: Dict,
                    n: int = 10):
    """
    Get top n largest values from the dictionary.

    Args:
        dictionary: Python dictionary
        n: Number of keys to pick

    Returns:

    """
    return top(dictionary, n=n)


def read_json(json_path: Union[str, Path]) -> Dict:
    """
    Read json file from a path.

    Args:
        json_path: File path to a json file.

    Returns:
        Python dictionary
    """
    with open(json_path, 'r') as fp:
        data = json.load(fp)
    return data


def write_json(item: Dict,
               path: Union[Path, str],
               mode: str = 'w') -> None:
    """
    Save json to a file.

    Args:
        item: Python dictionary
        path: File path to save at
        mode: File write mode

    Returns:
        None
    """
    with open(path, mode=mode) as fp:
        json.dump(item, fp)


def read_pickle(path: Union[str, Path]) -> Any:
    """
    Read a pickle file from path.

    Args:
        path: File path

    Returns:
        Unpickled object
    """
    with open(path, 'rb') as fp:
        return pickle.load(fp)


def write_pickle(item: Any,
                 path: Union[Path, str]) -> None:
    """
    Pickle a python object.

    Args:
        item: Python object
        path: File path to save the pickle file

    Returns:
        None
    """
    with open(path, 'wb') as fp:
        pickle.dump(item, fp)


def parse_manual(parser: argparse.ArgumentParser,
                 command: str) -> argparse.Namespace:
    """
    Use argument parser in notebooks.

    Args:
        parser: ArgumentParser
        command: Command line arguments as string

    Returns:
        Parsed argument as namespace
    """
    args = command.split()
    return parser.parse_args(args=args)


def hash_file(file_object: IO):
    """
    Calculate MD5 hash of file.

    Args:
        file_object: File object

    Returns:
        MD5 hash of the file
    """
    # Calculate hash
    unique_hash = md5_hash(file_object.read())

    # Reset file pointer to start
    file_object.seek(0)

    return unique_hash


def num_files(path: Union[Path, str]) -> int:
    """
    Get the number of files in a path.

    Args:
        path: File path

    Returns:
        Number of files
    """
    return len(os.listdir(path))
