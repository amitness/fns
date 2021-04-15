from pathlib import Path
from typing import Dict, List, Union

import pandas as pd
import numpy as np


def fake_df() -> pd.DataFrame:
    """
    Generate a dataframe filled with random data.

    Returns:
        Pandas DataFrame
    """
    return pd.util.testing.makeDataFrame()


def read_dict(data: Dict) -> pd.DataFrame:
    """
    Create a dataframe from dictionary with unequal elements.

    Args:
        data: Dictionary with column names as keys and rows as values

    Returns:
        Pandas DataFrame
    """
    return pd.DataFrame.from_dict(data, orient='index').transpose()


def print_groups(df: pd.DataFrame, column: str) -> None:
    """
    Pretty print all subsets of a groupby.

    Args:
        df: Pandas DataFrame
        column: Column Name to group by

    Returns:
        None
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

    Returns:
        None
    """
    import pandas as pd
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)


def no_wrapping():
    """
    Return a context manager to display all rows and columns.

    Examples:
    ```python
    with no_wrapping():
        print(df)
    ```

    Returns:
        Context Manager
    """
    return pd.option_context('display.max_rows', None,
                             'display.max_columns', None)


def explore_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform a quick peek of a dataframe.

    Currently shows:
    - Number of null elements in each column
    - Data type of each column
    - One example data for each column

    Args:
        df: Pandas DataFrame

    Returns:
        DataFrame with summary infos
    """
    null_df = pd.DataFrame(df.isnull().sum(), columns=['num_nulls'])
    dtype_df = pd.DataFrame(df.dtypes, columns=['dtype'])
    return (df.T.sample(1, axis=1)
            .join([dtype_df, null_df])
            .rename_axis('Columns')
            )


def is_outlier(values: List) -> List[bool]:
    """
    Generate a mask if an element is an outlier or not.

    Extra:
    ```
    Condition 1: < Q1 - 1.5 * IQR
    Condition 2: > Q3 + 1.5 * IQR
    ```

    Args:
        values: List of numerical values

    Returns:
        List of boolean indicating if an element is outlier or not
    """
    q1 = np.quantile(values, 0.25)
    q3 = np.quantile(values, 0.75)
    iqr = q3 - q1
    lower_threshold = q1 - 1.5 * iqr
    upper_threshold = q3 + 1.5 * iqr
    return (values < lower_threshold) | (values > upper_threshold)


def to_excel(path: Union[Path, str],
             df: pd.DataFrame,
             sheet_name: str,
             index: bool = False,
             mode: str = 'a') -> None:
    """
    Add a dataframe to an existing Excel file.

    Args:
        path: Path of the excel file
        df: Pandas DataFrame
        sheet_name: The sheet name to save in
        index: Keep or remove index
        mode: 'a' for append or 'w' for write

    Returns:
        None
    """
    with pd.ExcelWriter(path, mode=mode) as writer:
        df.to_excel(writer,
                    sheet_name=sheet_name,
                    index=index)
