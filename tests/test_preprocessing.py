from fns.preprocessing import remove_retweet, remove_hashtag, remove_hyperlink


def test_remove_retweet():
    assert remove_retweet('RT amazing') == 'amazing'


def test_remove_hashtag():
    assert remove_hashtag('#cool app') == 'cool app'


def test_remove_hyperlink():
    assert remove_hyperlink('https://google.com') == ''
