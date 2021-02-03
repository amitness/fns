import time
from typing import Callable


def timeit(func: Callable) -> Callable:
    """
    Decorator to calculate time taken for a function to complete.

    Args:
        func: Python Function

    Returns:
        Decorated function
    """
    start_time = time.time()

    def inner(*args, **kwargs):
        func(*args, **kwargs)
        total_time_taken = time.time() - start_time
        print('Total time taken: {} seconds'.format(total_time_taken))

    return inner


def show_shapes(fxn: Callable) -> Callable:
    """
    Decorator to log dataframe shape before and after applying a function.

    Args:
        fxn: Function that takes a dataframe as argument

    Returns:
        function
    """

    def inner(df):
        print(f'Shape before {fxn.__name__}', df.shape)
        out_df = fxn(df)
        print(f'Shape after {fxn.__name__}', out_df.shape)
        return out_df

    return inner


def deduplicate(fxn: Callable) -> Callable:
    """
    Decorator to deduplicate results of a function.

    Usage:
    ```python
    @deduplicate
    def test():
        return [1, 2, 3, 1]
    ```

    Args:
        fxn: Function

    Returns:
        Function
    """

    def inner(*args, **kwargs):
        return list(set(fxn(*args, **kwargs)))

    return inner
