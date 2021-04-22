from typing import List, Union

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline, FeatureUnion
from sklearn.preprocessing import FunctionTransformer

from fns.metrics import n_clusters


def cluster_text(texts: List[str],
                 return_dataframe: bool = True,
                 n: int = None) -> Union[pd.DataFrame, List[int]]:
    """
    Quickly cluster a list of sentences for EDA.

    Args:
        n: Number of clusters
        texts: List of sentences
        return_dataframe: Whether to return as dataframe or a list of cluster labels

    Returns:

    """
    n = n or n_clusters(texts)
    hybrid_tfidf = FeatureUnion([('word_tfidf', TfidfVectorizer(ngram_range=(1, 2),
                                                                strip_accents='unicode',
                                                                analyzer='word',
                                                                stop_words='english',
                                                                sublinear_tf=True)),
                                 ('char_tfidf', TfidfVectorizer(ngram_range=(3, 3),
                                                                strip_accents='unicode',
                                                                analyzer='char_wb',
                                                                stop_words='english',
                                                                sublinear_tf=True))])
    cluster_pipeline = make_pipeline(hybrid_tfidf,
                                     FunctionTransformer(lambda x: x.todense(), accept_sparse=True, validate=False),
                                     PCA(0.9, random_state=0),
                                     KMeans(n, random_state=0))
    clusters = cluster_pipeline.fit_predict(texts)
    if return_dataframe:
        return (pd.DataFrame({'text': texts, 'cluster': clusters})
                .assign(cluster_size=lambda d: d['cluster'].map(d['cluster'].value_counts()))
                .sort_values(by=['cluster_size', 'cluster', 'text'], ascending=[False, True, True])
                .drop(columns=['cluster_size']))
    else:
        return clusters


def similarity_sort(texts: List[str]) -> List[str]:
    """
    Sort list of sentences such that similar sentence are placed consecutively.

    Args:
        texts: List of sentences

    Returns:
        Sorted sentences
    """
    df = cluster_text(texts, n=len(texts) // 2)
    return df['text'].tolist()
