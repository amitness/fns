import time
from typing import Callable
import functools


def timeit(func: Callable) -> Callable:
    """
    Decorator to calculate time taken for a function to complete.

    Args:
        func: Python Function

    Returns:
        Decorated function
    """
    start_time = time.time()

    @functools.wraps(func)
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        total_time_taken = time.time() - start_time
        print('Total time taken: {} seconds'.format(total_time_taken))

    return inner


def show_shapes(func: Callable) -> Callable:
    """
    Decorator to log dataframe shape before and after applying a function.

    Args:
        func: Function that takes a dataframe as argument

    Returns:
        function
    """

    @functools.wraps(func)
    def inner(df):
        print(f'Shape before {func.__name__}', df.shape)
        out_df = func(df)
        print(f'Shape after {func.__name__}', out_df.shape)
        return out_df

    return inner


def deduplicate(func: Callable) -> Callable:
    """
    Decorator to deduplicate results of a function.

    Usage:
    ```python
    @deduplicate
    def test():
        return [1, 2, 3, 1]
    ```

    Args:
        func: Function

    Returns:
        Function
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        return list(set(func(*args, **kwargs)))

    return inner
