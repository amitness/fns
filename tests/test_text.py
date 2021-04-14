from fns.text import abbreviations


def test_abbreviations():
    assert abbreviations(['HTTP was used']) == ['HTTP']
