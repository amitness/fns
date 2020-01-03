from collections import Counter


def baseline_accuracy(labels):
    """Get accuracy for always majority class classifier.
    :type labels: list of class labels

    >>> baseline_accuracy([0, 1])
    50.0
    """
    (label, count), *_ = Counter(labels).most_common(1)
    return count / len(labels) * 100.0
