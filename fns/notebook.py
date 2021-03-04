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
