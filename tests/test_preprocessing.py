from fns.preprocessing import remove_retweet, remove_hashtag, remove_hyperlink, combine_hyphenated_word, \
    remove_multiple_commas


def test_remove_retweet():
    assert remove_retweet('RT amazing') == 'amazing'


def test_remove_hashtag():
    assert remove_hashtag('#cool app') == 'cool app'


def test_remove_hyperlink():
    assert remove_hyperlink('https://google.com') == ''


def test_combine_hyphenated_word():
    assert combine_hyphenated_word('e-mail me') == 'email me'
    assert combine_hyphenated_word('5-4 is 1') == '5-4 is 1'


def test_remove_multiple_commas():
    assert remove_multiple_commas('a,,b,c') == 'a,b,c'
