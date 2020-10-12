import re

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
