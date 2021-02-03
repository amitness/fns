from argparse import ArgumentParser, Namespace

from fns import parse_manual, flatten
from fns.text import window


def test_window():
    expected = [(['a', 'b'], 'c'), (['b', 'c'], 'd')]
    assert window(['a', 'b', 'c', 'd'], size=2) == expected


def test_parse_manual():
    parser = ArgumentParser()
    parser.add_argument('--n', type=int, required=True)
    args = parse_manual(parser, '--n 1')
    assert args == Namespace(n=1)


def test_flatten():
    assert list(flatten([[1], [2]])) == [1, 2]
