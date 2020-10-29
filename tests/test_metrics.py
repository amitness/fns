from fns.metrics import n_clusters


def test_n_clusters():
    assert n_clusters(4) == 2
