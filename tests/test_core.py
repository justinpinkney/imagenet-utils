from .context import imagenet_utils as imnet
import pytest
import pathlib

@pytest.fixture
def two_urls(monkeypatch):
    def mock_mapping(wnid):
        return "first\turl1\nsecond\turl2\n"
    monkeypatch.setattr(imnet.core, 'get_mapping', mock_mapping)
    
@pytest.fixture
def bad_url(monkeypatch):
    def mock_mapping(wnid):
        return "Invalid url!\n"
    monkeypatch.setattr(imnet.core, 'get_mapping', mock_mapping)

@pytest.fixture
def no_image_url(monkeypatch):
    def mock_mapping(wnid):
        return "\n"
    monkeypatch.setattr(imnet.core, 'get_mapping', mock_mapping)

@pytest.fixture
def good_content_type(monkeypatch):
    def mock_content_type(url):
        return "image/jpeg"
    monkeypatch.setattr(imnet.core, 'get_content_type', mock_content_type)

@pytest.fixture
def file_image_content(monkeypatch):
    def mock_fetch(url):
        test_image = pathlib.Path(__file__).with_name("test.jpg")
        with open(test_image, "rb") as im_file:
            image_content = im_file.read()
        return image_content
    monkeypatch.setattr(imnet.core, 'fetch_image', mock_fetch)

def test_query_match():
    words = "this is a test of searching"
    query = "test of"
    matched = imnet.match(query, words)
    assert matched

def test_search():
    result = imnet.search("taxus baccata")
    assert result[0].wnid == "n11661909"

def test_urls(two_urls):
    wnid = "n11661909"
    expected_length = 2

    urls = imnet.urls(wnid)

    assert len(urls) == expected_length

def test_bad_urls(bad_url):
    not_wnid = "not_wnid"
     
    with pytest.raises(ValueError):
        urls = imnet.urls(not_wnid)

def test_no_urls(no_image_url):

    not_wnid = "no_urls"
     
    with pytest.raises(ValueError):
        urls = imnet.urls(not_wnid)

def test_save_image(tmpdir, good_content_type, file_image_content):
    filename = "test"
    subdir = "folder"
    image = imnet.Image(filename, "")
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

