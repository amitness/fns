from fns.feature_extraction import HistogramEncoder


def test_histogram_encoder():
    encoder = HistogramEncoder()
    output = encoder.fit_transform(["hello", "world"])
    assert output.shape == (2, 256)
