from .context import imagenet_utils as imnet
import pytest

def test_search():
    result = imnet.search("taxus baccata")
    assert result[0].wnid == "n11661909"

def test_urls():
    wnid = "n11661909"
    expected_length = 636

    urls = imnet.urls(wnid)

    assert len(urls) == expected_length

def test_bad_urls():
    not_wnid = "not_wnid"
     
    with pytest.raises(ValueError):
        urls = imnet.urls(not_wnid)
