"""Core functions for donwloadingin imagenet urls"""
import os
from collections import namedtuple
from functools import lru_cache
import re

import requests

Synset = namedtuple('Synset', ['wnid', 'words'])
Image = namedtuple('Image', ['filename', 'url'])

@lru_cache()
def load_data():
    """Retrieve the wnid to words mapping."""
    words_file = os.path.join(os.path.dirname(__file__), "words.txt")

    with open(words_file) as out_file:
        lines = out_file.readlines()

    mapping = []
    for line in lines:
        data = line.strip().split("\t")
        mapping.append(Synset(wnid=data[0], words=data[1]))

    return mapping

def urls(wnid):
    """Return the list of Images for a given wnid."""

    url = "http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping"
    payload = {"wnid": wnid}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    result = response.text

    if result.strip() == "Invalid url!":
        raise ValueError(f"Unknown wnid '{wnid}'")
    elif result.strip() == "":
        # Some synsets are not available
        raise ValueError(f"wnid '{wnid}' is not available")
    else:
        images = []
        for line in result.strip().splitlines():
            elements = line.split()
            images.append(Image(filename=elements[0], url=elements[1]))
        return images


def save_image(image, destination):
    """Save the Image to a destination folder."""
    request_opts = {"timeout": 5,
                    "allow_redirects": False,
                    }
    # check it is an image
    image_check = requests.head(image.url, **request_opts)
    content_type = image_check.headers.get("Content-Type")

    if not content_type == "image/jpeg":
        raise ValueError(f"url not an image, instead type was {content_type}")

    response = requests.get(image.url, **request_opts)
    response.raise_for_status()
    content = response.content

    if not os.path.isdir(destination):
        os.mkdir(destination)

    filepath = os.path.join(destination, image.filename + ".jpg")
    with open(filepath, "wb") as out_file:
        out_file.write(content)


def download(wnid, destination):
    """Download images associated with a wnid."""
    image_urls = urls(wnid)
    print(len(image_urls))
    for image in image_urls:
        try:
            print(f"Downloading {image.filename}")
            save_image(image, destination)
        except (requests.exceptions.RequestException, ValueError):
            print(f"Could not retrieve image {image.filename}")


def match(search_query, words):
    query_words = search_query.split()
    return all(find_whole_word(query, words) for query in query_words)

def find_whole_word(query, words):
    """https://stackoverflow.com/a/5320179"""
    matches = re.compile(r'\b({0})\b'.format(query), flags=re.IGNORECASE).search(words)
    return matches is not None

def search(term):
    """Search for a term in the set of synset descriptions."""

    mapping = load_data()
    term = term.lower()

    results = []
    for index, entry in enumerate(mapping):
        if match(term, entry.words):
            results.append(mapping[index])

    return results

if __name__ == "__main__":
    trees = ["tilia x europaea",
             "ulmus minor var. vulgaris",
             "aesculus hippocastanum",
             "alnus glutinosa",
             "fraxinus excelsior",
             "populus tremula",
             "sorbus aucuparia",
             "quercus robur",
             "platanus x hispanica",
             "common fagus sylvatica",
             "pinus sylvestris",
             "salix fragilis",
             "acer campestre",
             "corylus avellana",
             "ilex aquifolium",
             "carpinus betulus",
             "quercus petraea",
             "betula pendula",
             "castanea sativa",
             "acer pseudoplatanus",
             "taxus baccata",
             ]

    for search_term in trees:
        print(search_term)
        tree_result = search(search_term)
        for r in tree_result:
            print(f"\t{r.wnid}\t{r.words}")

    download("n11661909", "test")
