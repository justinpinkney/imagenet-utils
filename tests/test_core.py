from .context import imagenet_utils as imnet
import pytest
import pathlib

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

def test_save_image(tmpdir):
    filename = "test"
    subdir = "folder"
    url = "http://image-net.org/nodes/11/07851298/ae/aec22f13c9abb26dc0b378e0f5f9d4fc5769e0ce.thumb"
    image = imnet.Image(filename, url)
    expected_path = pathlib.Path(tmpdir, subdir, filename + ".jpg")

    imnet.save_image(image, pathlib.Path(tmpdir, subdir))

    assert expected_path.is_file()

def test_save_not_image(tmpdir):
    filename = "test"
    subdir = "folder"
    url = "http://www.google.com"
    image = imnet.Image(filename, url)

    with pytest.raises(ValueError):
        imnet.save_image(image, pathlib.Path(tmpdir, subdir))

