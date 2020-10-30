import math
from collections import Counter
import numpy as np


def baseline_accuracy(labels):
    """Get accuracy for always majority class classifier.
    :type labels: list of class labels

    >>> baseline_accuracy([0, 1])
    50.0
    """
    (label, count), *_ = Counter(labels).most_common(1)
    return count / len(labels) * 100.0


def missing_value_percent(df):
    """
    Get the percentage of missing values in each column.
    :param df: Pandas DataFrame
    """
    num_rows = len(df)
    return (df.isna().sum() / num_rows * 100.0).sort_values(ascending=False)


def na_percent(df):
    return missing_value_percent(df)


def n_clusters(data):
    """
    Generate number of clusters to create.

    Heuristic:
    Number of clusters = square root of total data points

    :param data: Total number of data points or the data point itself
    :return:
    """
    if type(data) is int:
        total_rows = data
    else:
        total_rows = len(set(data))
    return int(math.sqrt(total_rows))


def vector_similarity(u, v):
    angle = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    return float(angle)
