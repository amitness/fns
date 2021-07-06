import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


def encode_histogram(text: str) -> np.ndarray:
    histogram = [0.0] * 256
    for ascii_code in text.encode("utf-8"):
        histogram[ascii_code] += 1
    return np.array(histogram) / len(text)


class HistogramEncoder(BaseEstimator, TransformerMixin):
    """
    Encode text into a bucket of 256 byte indices.
    """

    def __init__(self):
        super().__init__()

    def fit(self, *args, **kwargs):
        return self

    def transform(self, x):
        return np.stack([encode_histogram(e) for e in x])
