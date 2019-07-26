import time

def timeit(func):
    start_time = time.time()

    def inner(*args, **kwargs):
        func(*args, **kwargs)
        total_time_taken = time.time() - start_time
        print('Total time taken: {} seconds'.format(total_time_taken))
    return inner
