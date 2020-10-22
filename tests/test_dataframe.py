from fns.dataframe import read_dict


def test_read_dict():
    df = read_dict({'a': [1, 2, 3], 'b': [4, 5]})
    assert 'a' in df.columns
    assert 'b' in df.columns
    assert df['b'].isnull().sum() == 1
