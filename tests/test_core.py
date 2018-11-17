from .context import imagenet_utils as imnet

def test_search():
    result = imnet.search(imnet.load_data(), "taxus baccata")
    assert result[0].wnid == "n11661909"

