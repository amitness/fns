from typing import List
import pandas as pd


def print_markdown(markdown):
    from IPython.display import Markdown, display
    display(Markdown(markdown))


def print_bullets(lines: List[str]):
    bullet_points = '\n'.join(f'- `{line}`' for line in sorted(lines))
    print_markdown(bullet_points)


def print_header(text: str,
                 level: int = 2):
    print_markdown(f'{"#" * level} {text}')


def filter_column(df: pd.DataFrame,
                  column_name: str) -> None:
    """
    Show an interactive widget to filter a column in dataframe.

    Args:
        df: Pandas DataFrame
        column_name: Column Name of the DataFrame

    Returns:
        Interactive widget for filtering.
    """

    from ipywidgets import interact
    interact(lambda value: df[df[column_name] == value],
             value=df[column_name].unique())


def download_df(df: pd.DataFrame) -> None:
    """
    Generate a download link for a dataframe.

    The filename is set to a random UUID.

    Args:
        df: Pandas DataFrame

    Returns:
        None
    """
    from IPython.display import FileLink, display
    from uuid import uuid4
    random_csv_path = f'{uuid4()}.csv'
    df.to_csv(random_csv_path, index=False)
    display(FileLink(random_csv_path))
