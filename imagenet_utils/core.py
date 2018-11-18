import os
from collections import namedtuple
import requests
from functools import lru_cache

Synset = namedtuple('Synset', ['wnid', 'words'])

@lru_cache()
def load_data():
    """Retrieve the wnid to words mapping."""
    words_file = os.path.join(os.path.dirname(__file__), "words.txt")

    with open(words_file) as f:
        lines = f.readlines()

    mapping = []
    for line in lines:
        data = line.strip().split("\t")
        mapping.append(Synset(wnid=data[0], words=data[1]))

    return mapping

def urls(wnid):
    """Return the list of urls for a given wnid."""

    url = "http://www.image-net.org/api/text/imagenet.synset.geturls"
    payload = {"wnid": wnid}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    result = response.text

    if result.strip() == "Invalid url!":
        raise ValueError(f"Unknown wnid '{wnid}'")
    else:
        return result.split()

def search(term):
    """Search for a term in the set of synset descriptions."""

    mapping = load_data()
    term = term.lower()
    search_query = term.split()

    results = []
    for index, entry in enumerate(mapping):
        words = entry.words.lower()
        if all(query in words for query in search_query):
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
        result = search(search_term)
        for r in result:
            print(f"\t{r.wnid}\t{r.words}")

