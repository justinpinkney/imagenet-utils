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
    results = []
    for index, synset in enumerate(mapping):
        if term in synset.words:
            results.append(mapping[index])
    return results

if __name__ == "__main__":
    search_term = "Japanese oak"
    words = load_data()
    result = search(words, search_term)
    for r in result:
        print(r)
