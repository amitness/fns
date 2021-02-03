import hashlib
from typing import List


def md5_hash(text: str) -> str:
    """
    Generate MD5 hash of a text.

    Args:
        text: String

    Returns:
        MD5 hash
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def sha256hash(text: str) -> str:
    """
    Generate MD5 hash of a text.

    Args:
        text: String

    Returns:
        SHA256 hash
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def window(tokens,
           size: int = 3):
    """
    Generate samples for a window size.

    Example:
    ```python
    >>> window(['a', 'b', 'c', 'd'], size=2)
    [(['a', 'b'], 'c'), (['b', 'c'], 'd')]
    ```

    Args:
        tokens: List of tokens
        size: Window size

    Returns:
        List of windowed samples
    """
    return [(tokens[i: i + size], tokens[i + size])
            for i in range(0, len(tokens) - size, 1)]


def offset_by_one(x,
                  sequence_length: int = 3):
    """
    Generate a list of small sequences offset by 1.

    Usage:

    ```python
    >>> offset_by_one([1, 2, 3, 4, 5], sequence_length=3)
    [([1, 2, 3], [2, 3, 4])]
    ```

    Args:
        x: Python list
        sequence_length: Chunk size

    Returns:

    """
    sl = sequence_length
    return [(x[i:i + sl], x[i + 1:i + sl + 1])
            for i in range(0, len(x) - sl - 1, sl)]


def num_words(text: str) -> int:
    """
    Counts the number of words using whitespace as delimiter.

    Args:
        text: Sentence

    Returns:
        Number of words
    """
    return len(text.split())


def unique_chars(texts: List[str]) -> List[str]:
    """
    Get a list of unique characters from list of text.

    Args:
        texts: List of sentences

    Returns:
        A sorted list of unique characters
    """
    return sorted(set(''.join(texts)))


def is_non_ascii(text: str) -> bool:
    """
    Check if text has non-ascci characters.

    Useful heuristic to find text containing emojis and non-english
    characters.

    Args:
        text: Sentence

    Returns:
        True if the text contains non-ascii characters.
    """
    try:
        text.encode('ascii')
        return False
    except UnicodeEncodeError:
        return True
