import hashlib
import re
from typing import List, Tuple, Union

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd


def md5_hash(text: str) -> str:
    """
    Generate MD5 hash of a text.

    Args:
        text: String

    Returns:
        MD5 hash
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def sha256hash(text: str) -> str:
    """
    Generate MD5 hash of a text.

    Args:
        text: String

    Returns:
        SHA256 hash
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def window(tokens, size: int = 3):
    """
    Generate samples for a window size.

    Example:
    ```python
    >>> window(['a', 'b', 'c', 'd'], size=2)
    [(['a', 'b'], 'c'), (['b', 'c'], 'd')]
    ```

    Args:
        tokens: List of tokens
        size: Window size

    Returns:
        List of windowed samples
    """
    return [
        (tokens[i : i + size], tokens[i + size])
        for i in range(0, len(tokens) - size, 1)
    ]


def offset_by_one(x, sequence_length: int = 3):
    """
    Generate a list of small sequences offset by 1.

    Usage:

    ```python
    >>> offset_by_one([1, 2, 3, 4, 5], sequence_length=3)
    [([1, 2, 3], [2, 3, 4])]
    ```

    Args:
        x: Python list
        sequence_length: Chunk size

    Returns:

    """
    sl = sequence_length
    return [
        (x[i : i + sl], x[i + 1 : i + sl + 1]) for i in range(0, len(x) - sl - 1, sl)
    ]


def num_words(text: str) -> int:
    """
    Counts the number of words using whitespace as delimiter.

    Args:
        text: Sentence

    Returns:
        Number of words
    """
    return len(text.split())


def unique_chars(texts: List[str]) -> List[str]:
    """
    Get a list of unique characters from list of text.

    Args:
        texts: List of sentences

    Returns:
        A sorted list of unique characters
    """
    return sorted(set("".join(texts)))


def is_non_ascii(text: str) -> bool:
    """
    Check if text has non-ascci characters.

    Useful heuristic to find text containing emojis and non-english
    characters.

    Args:
        text: Sentence

    Returns:
        True if the text contains non-ascii characters.
    """
    try:
        text.encode("ascii")
        return False
    except UnicodeEncodeError:
        return True


def span_positions(text: str, phrases: List[str]) -> List[Tuple[int, int]]:
    """
    Find span position of phrases in a text.

    Args:
        text: Sentence
        phrases: List of phrases

    Returns:
        List of span positions for each phrase.
        The span position is a tuple of start and end index.
    """
    capture_group = "|".join([re.escape(phrase) for phrase in phrases])
    reg = re.compile(rf"\b({capture_group})\b", flags=re.IGNORECASE)
    return [match.span() for match in reg.finditer(text)]


def extract_abbreviations(texts: List[str]) -> List[str]:
    """
    Get a list of all-capitalized words.

    Example: WWW, HTTP, etc.

    Args:
        texts: List of sentences

    Returns:
        List of abbreviations
    """
    combined_text = "\n".join(texts)
    symbols = re.findall(r"\b[A-Z][A-Z]+\b", combined_text)
    return list(set(symbols))


def export_fasttext_format(
    texts: List[str], labels: Union[List[str], List[List[str]]], filename
) -> None:
    """
    Export training data to a fasttext compatible format.

    Format:
    __label__POSITIVE it was good

    Args:
        texts: List of sentences
        labels: List of single or multi-label classes
        filename: Exported filename

    Returns:
        None
    """
    output = []
    for text, text_label in zip(texts, labels):
        if type(text_label) is str:
            text_label = [text_label]
        labels = " ".join([f"__label__{label}" for label in text_label])
        output.append(f"{labels} {text}\n")
    with open(filename, "w") as fp:
        fp.writelines(output)


def extract_tfidf_keywords(texts: List[str], ngram: int = 2, n: int = 10) -> List[str]:
    """
    Get top keywords based on mean tf-idf term score.

    Args:
        texts: List of sentences
        ngram: 1 for words, 2 for bigram and so on.
        n: Number of keywords to extract

    Returns:
        Keywords
    """
    tfidf = TfidfVectorizer(
        ngram_range=(1, ngram),
        stop_words="english",
        strip_accents="unicode",
        sublinear_tf=True,
    )
    vectors = tfidf.fit_transform(texts)
    term_tfidf = vectors.A.mean(axis=0)
    terms = np.array(tfidf.get_feature_names())
    return terms[term_tfidf.argsort()[::-1]][:n].tolist()


def extract_discriminative_keywords(
    df: pd.DataFrame,
    category_column: str,
    text_column: str,
    ngram: int = 2,
    n: int = 10,
) -> pd.DataFrame:
    """
    Generate discriminative keywords for texts in each category.

    Args:
        df: Dataframe with text and category columns.
        text_column: Column name containing texts
        category_column: Column name for the text category
        ngram: 1 for words, 2 for bigram and so on.
        n: Number of keywords to return.

    Returns:
        Dataframe with categories in columns and top-n keywords in each columns.
    """
    # Combine all texts into a single document for each category
    category_docs = df.groupby(by=category_column)[text_column].apply(" ".join)
    categories = category_docs.index.tolist()

    tfidf = TfidfVectorizer(
        ngram_range=(1, ngram),
        stop_words="english",
        strip_accents="unicode",
        sublinear_tf=True,
    )
    document_vectors = tfidf.fit_transform(category_docs).A
    keywords = np.array(tfidf.get_feature_names())
    top_terms = document_vectors.argsort(axis=1)[:, :n]
    return pd.DataFrame(keywords[top_terms].T, columns=categories)


def extract_stopwords(texts: List[str]) -> pd.DataFrame:
    vec = TfidfVectorizer()
    vec.fit(texts)
    word_idf_pairs = zip(vec.get_feature_names(), vec.idf_)
    return pd.DataFrame(word_idf_pairs, columns=["word", "idf"]).sort_values(by="idf")
