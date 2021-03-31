from typing import List, Union

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


def highlight_phrases(original_text: str,
                      phrases: Union[List[str], str],
                      color_palette: str = 'Greens',
                      weight: float = 0.2) -> None:
    """
    Highlight a list of phrases in a text.

    Args:
        original_text: Sentence
        phrases: A single phrase or a list of phrases
        color_palette: Any valid matplotlib color palette name
        weight: Darkness of the color

    Returns:
        None
    """
    import matplotlib.cm
    from IPython.display import HTML, display

    html = original_text
    cmap = matplotlib.cm.get_cmap(color_palette)
    color = f'rgba{cmap(weight, bytes=True)}'
    if type(phrases) is str:
        phrases = [phrases]
    for phrase in phrases:
        highlighted_phrase = (f'<span style="background-color: {color}; font-weight: {weight * 800};">'
                              f'{phrase}'
                              f'</span>')
        html = html.replace(phrase, highlighted_phrase)
    display(HTML(f'<p style="color: #444; font-size:1.5em;">{html}</p>'))


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
