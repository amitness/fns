import base64
import csv


def create_download_link(dataframe,
                         filename: str,
                         file_type: str = 'csv',
                         index: bool = False,
                         header: bool = True):
    """
    Generate a download link for a pandas dataframe.

    Args:
        dataframe: Pandas DataFrame
        filename: Name of exported file
        file_type: Either 'csv' or 'tsv'
        index: Whether to include index of dataframe or not
        header: Whether to include header of dataframe or not

    Returns:
        Markdown to place in st.markdown(...)
    """
    if file_type == 'csv':
        dataframe_csv = dataframe.to_csv(index=index)
    elif file_type == 'tsv':
        dataframe_csv = dataframe.to_csv(index=index,
                                         sep='\t',
                                         header=header,
                                         quoting=csv.QUOTE_NONNUMERIC)
    else:
        raise Exception('Invalid file_type. Allowed values are "csv" and "tsv".')

    b64 = base64.b64encode(dataframe_csv.encode()).decode()
    href = f'**DOWNLOAD:** <a href="data:file/csv;base64,{b64}" download="{filename}">{filename}</a>'
    return href
