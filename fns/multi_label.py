from typing import List

from sklearn.preprocessing import MultiLabelBinarizer


def validate_multiple_labels(y_raw: List[List]) -> None:
    """
    Validate binarization of labels in a multi-label setting.

    Args:
        y_raw: Raw list of list of labels.

    Returns:

    """
    y = MultiLabelBinarizer().fit_transform(y_raw)

    # Assert that every sample has atleast one label
    assert (y.sum(axis=1) == 0).sum() == 0

    # Assert that every label is assigned to some data point
    assert (y.sum(axis=0) == 0).sum() == 0

    # Assert that no label is assigned to only one data point
    assert (y.sum(axis=0) == 1).any() is False
