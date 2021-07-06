from fns.text import extract_abbreviations


def test_abbreviations():
    assert extract_abbreviations(["HTTP was used"]) == ["HTTP"]
