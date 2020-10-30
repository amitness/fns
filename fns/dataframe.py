from typing import Dict

import pandas as pd


def read_dict(data: Dict):
    """
    Create a dataframe from dictionary with unequal elements.
    :param data: Dictionary with column names as keys and rows as values
    :return: Pandas DataFrame
    """
    return pd.DataFrame.from_dict(data, orient='index').transpose()


def print_groups(df: pd.DataFrame, column: str) -> None:
    """
    Pretty print
    Parameters
    ----------
    df: Pandas DataFrame
    column: Column Name to group by

    Returns
    -------

    """
    for current_group, sub_df in df.groupby(column):
        print(f'Group: {current_group}')
        print()
        print(sub_df)
        print()
        print('---' * 25)


def display_all() -> None:
    """
    Show all the rows and columns when printing dataframe.

    Returns None
    -------
    """
    import pandas as pd
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
