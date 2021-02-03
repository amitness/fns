import math
from collections import Counter
from typing import Dict, Callable, List

import numpy as np
import timeit


def benchmark_function(fn: Callable,
                       repeat: int = 5) -> Dict:
    """
    Benchmark time taken for a function and return metrics.

    Args:
        fn: A python function
        repeat: Number of samples

    Returns:
        Dictionary of total times, mean and std of times
    """
    iteration_times = timeit.repeat(fn,
                                    repeat=repeat,
                                    number=1)
    return {'time': iteration_times,
            'mean': np.mean(iteration_times),
            'std': np.std(iteration_times)}


def baseline_accuracy(labels: List) -> float:
    """
    Get accuracy for always majority class classifier.

    Usage:
    ```python
    >>> baseline_accuracy([0, 1])
    50.0
    ```

    Args:
        labels: List of class labels.

    Returns:
        Baseline accuracy
    """
    (label, count), *_ = Counter(labels).most_common(1)
    return count / len(labels) * 100.0


def missing_value_percent(df):
    """
    Get the percentage of missing values in each column.

    Args:
        df: Pandas DataFrame

    Returns:
        Percentage of missing value in each column.
    """
    num_rows = len(df)
    return (df.isna().sum() / num_rows * 100.0).sort_values(ascending=False)


def na_percent(df):
    return missing_value_percent(df)


def n_clusters(data) -> int:
    """
    Generate number of clusters to create.

    Heuristic:
    Number of clusters = square root of total data points

    Args:
        data: Total number of data points or the data point itself

    Returns:
        Number of clusters
    """
    if type(data) is int:
        total_rows = data
    else:
        total_rows = len(set(data))
    return int(math.sqrt(total_rows))


def vector_similarity(u, v) -> float:
    angle = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    return float(angle)
