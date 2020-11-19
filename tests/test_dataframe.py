from fns.dataframe import read_dict, is_outlier
import numpy as np


def test_read_dict():
    df = read_dict({'a': [1, 2, 3], 'b': [4, 5]})
    assert 'a' in df.columns
    assert 'b' in df.columns
    assert df['b'].isnull().sum() == 1


def test_is_outlier():
    data = np.array([1, 2, 3, 100, 200, 100000])
    expected = np.array([False, False, False, False, False, True])
    assert (is_outlier(data) == expected).all()
