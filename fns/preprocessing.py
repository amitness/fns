import json
import re
import string
from typing import Dict

from fns.json_encoders import NpEncoder

# Compiled regular expressions
_re_space = re.compile(r' {2,}')
_re_hashtag = re.compile(r'#')
_re_retweet = re.compile(r'^RT[\s]+')
_re_hyperlink = re.compile(r'https?:\/\/.*[\r\n]*')
_re_hyphen_word = re.compile('[a-zA-Z]+-[a-zA-Z]+')
_re_comma = re.compile(r',{2,}')


def combine_hyphenated_word(text: str) -> str:
    """
    Combine words in text that contain hyphen.

    Example: e-email to email

    Args:
        text: A sentence

    Returns:
        Processed sentence
    """
    return ' '.join(w.replace('-', '') if _re_hyphen_word.match(w) else w
                    for w in text.split())


def remove_hashtag(t: str) -> str:
    """
    Remove hashtag from the text.

    Args:
        t: Text

    Returns:
        Text without hashtag
    """
    return _re_hashtag.sub('', t)


def remove_retweet(t: str) -> str:
    """
    Remove RT from the text.

    Args:
        t: Text

    Returns:
        Text without RT symbol.
    """
    return _re_retweet.sub('', t)


def remove_hyperlink(t: str) -> str:
    """
    Remove hyperlinks from a text.

    Args:
        t: Text

    Returns:
        Text without hyperlinks.
    """
    return _re_hyperlink.sub('', t)


def remove_multiple_space(t: str) -> str:
    """
    Remove multiple spaces from the text.

    Adapted from: https://github.com/fastai/fastai/blob/master/fastai/text/core.py

    Args:
        t: Text

    Returns:
        Text without multiple space.
    """
    return _re_space.sub(' ', t)


def remove_multiple_commas(t: str) -> str:
    """
    Substitute multiple consecutive commas with a single comma.

    Usage:
    ```python
    >>> remove_multiple_commas('a,,b,c')
    'a,b,c'
    ```

    Args:
        t: Text

    Returns:
        Text without multiple commas.
    """
    return _re_comma.sub(',', t)


def remove_new_lines(text: str) -> str:
    """
    Strip away new lines at end.

    Args:
        t: Text

    Returns:
        Text without newline at end.
    """
    if isinstance(text, str):
        return text.replace('\\n', '').strip()
    return text


def remove_punctuation(text: str) -> str:
    """
    Remove all punctuations from a text.

    Args:
        text: Sentence

    """
    return ''.join(t for t in text if t not in string.punctuation)


def normalize_json(json_data: Dict) -> Dict:
    """
    Convert any non-standard types in dictionary to basic types.

    The normalization prevent errors during serialization.

    Usage:
    ```python
    >>> normalize_json({'nums': np.array([1, 2, 3]})
    {'nums': [1, 2, 3]}
    ```

    Args:
        json_data: Dictionary

    Returns:
        Normalized dictionary
    """
    return json.loads(json.dumps(json_data, cls=NpEncoder))
