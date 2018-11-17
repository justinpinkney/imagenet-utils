import os
from collections import namedtuple

Synset = namedtuple('Synset', ['wnid', 'words'])

def load_data():
    words_file = os.path.join(os.path.dirname(__file__), "words.txt")

    with open(words_file) as f:
        lines = f.readlines()

    mapping = []
    for line in lines:
        data = line.strip().split("\t")
        mapping.append(Synset(wnid=data[0], words=data[1]))

    return mapping


def search(mapping, term):
    term = term.lower()
    results = []
    search_query = term.split()
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

    words = load_data()
    for search_term in trees:
        print(search_term)
        result = search(words, search_term)
        for r in result:
            print(f"\t{r.wnid}\t{r.words}")
