import time


def timeit(func):
    start_time = time.time()

    def inner(*args, **kwargs):
        func(*args, **kwargs)
        total_time_taken = time.time() - start_time
        print('Total time taken: {} seconds'.format(total_time_taken))

    return inner


def show_shapes(fxn):
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


def deduplicate(f):
    """
    Decorator to deduplicate results of a function.

    Usage:
    ```python
    @deduplicate
    def test():
        return [1, 2, 3, 1]
    ```

    Args:
        f: Function

    Returns:
        Function
    """

    def inner(*args, **kwargs):
        return list(set(f(*args, **kwargs)))

    return inner
