import json
import re

from fns.json_encoders import NpEncoder

# Compiled regular expressions
_re_space = re.compile(' {2,}')


def remove_multiple_space(t: str) -> str:
    """
    Remove multiple spaces from the text.

    Modified from: https://github.com/fastai/fastai/blob/master/fastai/text/core.py
    """
    return _re_space.sub(' ', t)


def remove_new_lines(text: str) -> str:
    """
    Strip away new lines at end.
    """
    if isinstance(text, str):
        return text.replace('\\n', '').strip()
    return text


def normalize_json(json_data):
    """
    Convert any non-standard types in dictionary to basic types.

    The normalization prevent errors during serialization.

    Example:
    {'nums': np.array([1, 2, 3]} -> {'nums': [1, 2, 3]}

    :param json_data: Dictionary
    :return: Normalized dictionary
    """
    return json.loads(json.dumps(json_data, cls=NpEncoder))
