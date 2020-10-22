from typing import Dict

import pandas as pd


def read_dict(data: Dict):
    """
    Create a dataframe from dictionary with unequal elements.
    :param data: Dictionary with column names as keys and rows as values
    :return: Pandas DataFrame
    """
    return pd.DataFrame.from_dict(data, orient='index').transpose()
