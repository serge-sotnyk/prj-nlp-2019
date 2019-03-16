import spacy
from spacy import displacy

parse = {
    'words': [
        {'text': '6с', 'tag': 'NOUN'},
        {'text': 'приземляється', 'tag': 'VERB'},
        {'text': 'на', 'tag': 'IN'},
        {'text': 'плече', 'tag': 'NOUN'},
        {'text': ',', 'tag': 'PUNCT'},
        {'text': 'перекочуючись', 'tag': 'VERB'},
        {'text': ',', 'tag': 'PUNCT'},
        {'text': 'пролітає', 'tag': 'VERB'},
        {'text': 'метрів', 'tag': 'NOUN'},
        {'text': 'пʼятдесят', 'tag': 'NUM'},
        {'text': 'і', 'tag': 'CCONJ'},
        {'text': 'витягується', 'tag': 'VERB'},
        {'text': 'на', 'tag': 'IN'},
        {'text': 'снігу', 'tag': 'NOUN'},
        {'text': 'за', 'tag': 'ADP'},
        {'text': 'кілька', 'tag': 'NUM'},
        {'text': 'кроків', 'tag': 'NOUN'},
        {'text': 'від', 'tag': 'ADP'},
        {'text': 'забризканої', 'tag': 'ADJ'},
        {'text': 'палаючими', 'tag': 'ADJ'},
        {'text': 'уламками', 'tag': 'NOUN'},
        {'text': 'посадкової', 'tag': 'ADJ'},
        {'text': 'смуги', 'tag': 'NOUN'},
        {'text': '.', 'tag': 'PUNCT'},
    ],
    'arcs': [
        {'start': 0, 'end': 1, 'label': 'nsubj', 'dir': 'left'},
        {'start': 1, 'end': 2, 'label': 'prep', 'dir': 'right'},
        {'start': 1, 'end': 5, 'label': 'advmod', 'dir': 'right'},
        {'start': 1, 'end': 7, 'label': 'conj', 'dir': 'right'},
        {'start': 1, 'end': 4, 'label': 'punct', 'dir': 'right'},
        {'start': 1, 'end': 6, 'label': 'punct', 'dir': 'right'},
        {'start': 1, 'end': 23, 'label': 'punct', 'dir': 'right'},
        {'start': 2, 'end': 3, 'label': 'pobj', 'dir': 'right'},
        {'start': 7, 'end': 8, 'label': 'dobj', 'dir': 'right'},
        {'start': 7, 'end': 10, 'label': 'cc', 'dir': 'right'},
        {'start': 7, 'end': 11, 'label': 'conj', 'dir': 'right'},
        {'start': 8, 'end': 9, 'label': 'nummod', 'dir': 'right'},
        {'start': 11, 'end': 12, 'label': 'prep', 'dir': 'right'},
        {'start': 11, 'end': 14, 'label': 'prep', 'dir': 'right'},
        {'start': 12, 'end': 13, 'label': 'pobj', 'dir': 'right'},
        {'start': 15, 'end': 16, 'label': 'amod', 'dir': 'left'},
        {'start': 16, 'end': 17, 'label': 'prep', 'dir': 'right'},
        {'start': 17, 'end': 22, 'label': 'pobj', 'dir': 'right'},
        {'start': 18, 'end': 20, 'label': 'amod', 'dir': 'right'},
        {'start': 18, 'end': 22, 'label': 'amod', 'dir': 'left'},
        {'start': 19, 'end': 20, 'label': 'amod', 'dir': 'left'},
        {'start': 21, 'end': 22, 'label': 'amod', 'dir': 'left'},
    ]
}

displacy.serve(parse, manual=True)

