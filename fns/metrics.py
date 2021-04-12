import math
from collections import Counter
from typing import Dict, Callable, List

import numpy as np
import timeit

import pandas as pd
from sklearn import metrics as M


def clustering_report(y_true, y_pred) -> pd.DataFrame:
    """
    Generate cluster evaluation metrics.

    Args:
        y_true: Array of actual labels
        y_pred: Array of predicted clusters

    Returns:
        Pandas DataFrame with metrics.
    """
    return pd.DataFrame({
        'Homogeneity': M.homogeneity_score(y_true, y_pred),
        'Completeness': M.completeness_score(y_true, y_pred),
        'V-Measure': M.v_measure_score(y_true, y_pred),
        'Adjusted Rand Index': M.adjusted_rand_score(y_true, y_pred),
        'Adjusted Mutual Information': M.adjusted_mutual_info_score(y_true, y_pred)
    }, index=['value']).T


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


def jaccard(x, y) -> float:
    """
    Compute jaccard similarity (intersection over union).

    Args:
        x: Array-like object
        y: Array-like object

    Returns:
        Intersection Over Union score
    """
    s1 = set(x)
    s2 = set(y)
    if len(s1) == 0 and len(s2) == 0:
        return 0
    return len(s1 & s2) / len(s1 | s2)


def sorted_classification_report(y_true, y_pred, **kwargs) -> pd.DataFrame:
    """
    Generate class-wise classification report sorted from worst to best.

    Args:
        y_true: Actual labels
        y_pred: Predicted labels

    Returns:
        Classification report in sorted form.
    """
    base_report = M.classification_report(y_true,
                                          y_pred,
                                          output_dict=True,
                                          **kwargs)
    base_report_df = pd.DataFrame.from_dict(base_report).T
    class_wise_df = (base_report_df
                     .iloc[:-3]
                     .sort_values(by='f1-score'))
    summary_df = base_report_df.iloc[-3:]
    combined_df = pd.concat([class_wise_df, summary_df])
    combined_df['support'] = combined_df['support'].astype(int)
    return combined_df
