from fns.metrics import n_clusters, baseline_accuracy, jaccard, sorted_classification_report


def test_n_clusters():
    assert n_clusters(4) == 2


def test_baseline_accuracy():
    assert baseline_accuracy([1, 1, 1, 0]) == 75.0


def test_jaccard():
    assert jaccard([1, 2, 3, 4], [1, 2, 3]) == 0.75


def test_sorted_classification_report():
    report = sorted_classification_report([1, 1, 0], [1, 0, 1])
    assert report.shape == (5, 4)
