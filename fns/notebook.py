from typing import List, Union

import pandas as pd


def print_markdown(markdown):
    from IPython.display import Markdown, display
    display(Markdown(markdown))


def print_bullets(lines: List[str]) -> None:
    """
    Display a list of text as bullet points.

    Args:
        lines: List of texts

    Returns:
        None
    """
    bullet_points = '\n'.join(f'- `{line}`' for line in sorted(lines))
    print_markdown(bullet_points)


def print_header(text: str,
                 level: int = 2) -> None:
    """
    Display a text as markdown header.

    Args:
        text: Text
        level: 2 for H2, 3 for H3 upto 6.

    Returns:
        None
    """
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
    options = sorted(df[column_name].unique())
    interact(lambda value: df[df[column_name] == value],
             value=options)


def download_df(df: pd.DataFrame,
                csv_path=None) -> None:
    """
    Download a dataframe as a CSV with a random filename.

    The filename is set to a random UUID.

    Args:
        df: Pandas DataFrame
        csv_path: CSV filename.

    Returns:
        None
    """
    from IPython.display import Javascript
    if not csv_path:
        from uuid import uuid4
        csv_path = f'{uuid4()}.csv'
    df.to_csv(csv_path, index=False)
    script = f'''
            var location = window.location.host;
            var download_link = window.location.protocol + "//" + location + "/files/{csv_path}"
            window.open(download_link)
            '''
    return Javascript(script)


def search_dataframe(df: pd.DataFrame) -> None:
    """
    Show an interactive widget to search text fields of a dataframe.

    Args:
        df: Pandas DataFrame

    Returns:
        Interactive widget for searching.
    """

    from ipywidgets import interact
    from IPython.display import display

    def _search(query: str, column: str):
        if query:
            with pd.option_context('display.max_rows', None,
                                   'display.max_columns', None):
                filtered_df = df[df[column].str.contains(query,
                                                         case=False,
                                                         regex=False)]
                display(filtered_df)

    string_columns = df.select_dtypes('object').columns.tolist()
    interact(_search, query='', column=string_columns)
