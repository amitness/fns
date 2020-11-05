import hashlib
from typing import List


def md5_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def sha256hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def window(tokens, size=3):
    return [(tokens[i: i + size], tokens[i + size])
            for i in range(0, len(tokens) - size, 1)]


def offset_by_one(x, sequence_length=3):
    """
    :param x: Python list
    :param sequence_length: Chunk size

    >>> offset_by_one([1, 2, 3, 4, 5], sequence_length=3)
    [([1, 2, 3], [2, 3, 4])]

    """
    sl = sequence_length
    return [(x[i:i + sl], x[i + 1:i + sl + 1])
            for i in range(0, len(x) - sl - 1, sl)]


def num_words(text: str):
    """
    Counts the number of words using whitespace as delimiter.

    :param text: Sentence
    :return: Number of words
    """
    return len(text.split())


def unique_chars(texts: List[str]):
    """
    Get a list of unique characters from list of text.
    """
    return sorted(set(''.join(texts)))
