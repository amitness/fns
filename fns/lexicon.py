from functools import lru_cache
from pathlib import Path
from typing import List

import pandas as pd
import numpy as np

NEGATION_WORDS = [
    "no",
    "not",
    "never",
    "none",
    "nothing",
    "nobody",
    "neither",
    "nowhere",
    "hardly",
    "scarcely",
    "barely",
    "doesn’t",
    "isn’t",
    "wasn’t",
    "shouldn’t",
    "wouldn’t",
    "couldn’t",
    "won’t",
    "can't",
    "don't",
]

INTERROGATIVE_WORDS = ["what", "who", "when", "where", "which", "why", "how"]

TENTATIVE_WORDS = [
    "appears to",
    "can",
    "could",
    "it is likely",
    "it is possible",
    "it is probable",
    "it is unlikely",
    "may",
    "might",
    "possibly",
    "probably",
    "seems to",
    "suggests that",
    "tends to",
]

REASON_WORDS = ["because", "reason", "as a result", "since", "therefore"]


@lru_cache(1)
def onegram_count() -> pd.DataFrame:
    """
    Get counts of 1-gram from Peter Norvig's list.

    Returns:
        DataFrame with one-gram, count and idf scores.
    """
    df = pd.read_csv(
        "https://norvig.com/ngrams/count_1w.txt",
        sep="\t",
        header=None,
        names=["word", "count"],
    )
    df["idf"] = np.log(df["count"].sum() / df["count"])
    df.sort_values(by="idf", ascending=True, inplace=True)
    return df


@lru_cache(1)
def bigram_count():
    # Fetch ngram counts from remote path
    url = "https://norvig.com/ngrams/count_2w.txt"
    bigram_df = pd.read_csv(url, sep="\t", names=["bigram", "count"])

    # Split bigram into separate columns
    bigram_df[["word1", "word2"]] = bigram_df.bigram.str.split(expand=True)
    return bigram_df


@lru_cache(1)
def nrc_vad() -> pd.DataFrame:
    url = "https://github.com/nchibana/moviearcs/raw/master/NRC-VAD-Lexicon.txt"
    return pd.read_csv(url, sep="\t")


def dict_words() -> List[str]:
    """
    Fetch default list of words present in Linux distros.

    Returns:
        List of words
    """
    return Path("/usr/share/dict/words").read_text().splitlines()
