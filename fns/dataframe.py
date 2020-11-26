from typing import Dict

import pandas as pd
import numpy as np


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


def explore_df(df):
    null_df = pd.DataFrame(df.isnull().sum(), columns=['num_nulls'])
    dtype_df = pd.DataFrame(df.dtypes, columns=['dtype'])
    return (df.T.sample(1, axis=1)
            .join([dtype_df, null_df])
            .rename_axis('Columns')
            )


def is_outlier(values):
    q1 = np.quantile(values, 0.25)
    q3 = np.quantile(values, 0.75)
    iqr = q3 - q1
    lower_threshold = q1 - 1.5 * iqr
    upper_threshold = q3 + 1.5 * iqr
    return (values < lower_threshold) | (values > upper_threshold)


def to_excel(path: str, df,
             sheet_name: str,
             index: bool = False,
             mode: str = 'a') -> None:
    """
    Add a dataframe to an existing Excel file.

    Parameters
    ----------
    path: Path of the excel file
    df: Pandas DataFrame
    sheet_name: The sheet name to save in
    index: Save or remove index
    mode: 'a' for append or 'w' for write

    Returns: None
    -------
    """
    with pd.ExcelWriter(path, mode=mode) as writer:
        df.to_excel(writer,
                    sheet_name=sheet_name,
                    index=index)
