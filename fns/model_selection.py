from typing import Tuple

import pandas as pd


def train_val_size(dataset,
                   val_ratio: float = 0.1) -> Tuple[int, int]:
    """
    Return the train and validation data sizes based on split ratio.

    Args:
        dataset: A python collection
        val_ratio: Ratio for validation dataset

    Returns:
        Tuple of number of rows for (training, validation)
    """
    val_size = int(val_ratio * len(dataset))
    train_size = len(dataset) - val_size
    return train_size, val_size


def view_result_table(cv) -> pd.DataFrame:
    """
    Display results from cross-validation.

    Args:
        cv: Result of cross-validation

    Returns:
        Pandas DataFrame
    """
    columns = ['params', 'mean_test_score', 'std_test_score', 'rank_test_score']
    return (pd.DataFrame(cv.cv_results_)[columns]
            .sort_values(by=['rank_test_score'])
            )
