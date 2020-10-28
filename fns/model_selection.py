import pandas as pd


def train_val_size(dataset, val_ratio=0.1):
    """
    Return the train and validation data sizes based on split ratio.
    :param dataset:
    :param val_ratio: Ratio for validation dataset
    :return:
    """
    val_size = int(val_ratio * len(dataset))
    train_size = len(dataset) - val_size
    return train_size, val_size


def view_result_table(cv):
    columns = ['params', 'mean_test_score', 'std_test_score', 'rank_test_score']
    return (pd.DataFrame(cv.cv_results_)[columns]
            .sort_values(by=['rank_test_score'])
            )
