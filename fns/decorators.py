import time


def timeit(func):
    start_time = time.time()

    def inner(*args, **kwargs):
        func(*args, **kwargs)
        total_time_taken = time.time() - start_time
        print('Total time taken: {} seconds'.format(total_time_taken))

    return inner


def show_shapes(fxn):
    def inner(df):
        print(f'Shape before {fxn.__name__}', df.shape)
        out_df = fxn(df)
        print(f'Shape after {fxn.__name__}', out_df.shape)
        return out_df

    return inner
