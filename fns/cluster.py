from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

from .metrics import n_clusters
from sklearn.pipeline import Pipeline
import pandas as pd


def cluster_text(texts,
                 embedding: str = 'tf-idf',
                 return_dataframe=True):
    n = n_clusters(texts)
    if embedding == 'tf-idf':
        vectorizer = TfidfVectorizer(strip_accents='ascii',
                                     stop_words='english',
                                     sublinear_tf=True)
    elif embedding == 'count':
        vectorizer = CountVectorizer(strip_accents='ascii',
                                     stop_words='english')
    else:
        raise Exception('Invalid argument for embedding')

    cluster_pipeline = Pipeline([
        ('vectorizer', vectorizer),
        ('pca', TruncatedSVD()),
        ('kmeans', KMeans(n))
    ])
    clusters = cluster_pipeline.fit_predict(texts)
    if return_dataframe:
        return pd.DataFrame({'text': texts, 'cluster': clusters})
    else:
        return clusters
