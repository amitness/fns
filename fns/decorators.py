import time
from typing import Callable
import functools

from fns import minibatch


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


def batched(batch_size: int = 32) -> Callable:
    """
    Apply a function over small batches of a list and combine results.

    Args:
        batch_size: Size of each mini-batch

    Returns:
        Decorator for the batch size
    """

    def decorator(func) -> Callable:
        @functools.wraps(func)
        def inner(*args, **kwargs):
            items = args[0]
            results = []
            for batch in minibatch(items, batch_size):
                batch_results = func(batch)
                results.extend(batch_results)
            return results

        return inner

    return decorator


def to(data_type) -> Callable:
    """
    Apply a data type to returned data from a function.

    Args:
        data_type: The data type to apply. Eg: list, int etc.

    Returns:
        Decorator that applies the data type on returned data
    """

    def decorator(func) -> Callable:
        @functools.wraps(func)
        def inner(*args, **kwargs):
            return data_type(func(*args, **kwargs))

        return inner

    return decorator
