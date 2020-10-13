from fns.text import window


def test_window():
    expected = [(['a', 'b'], 'c'), (['b', 'c'], 'd')]
    assert window(['a', 'b', 'c', 'd'], size=2) == expected
