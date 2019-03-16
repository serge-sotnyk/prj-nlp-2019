import spacy
from collections import defaultdict

nlp = spacy.load('en_core_web_lg', disable=['ner', 'textcat'])

synonyms = {'announce', 'answer', 'assert', 'claim', 'convey', 'declare', 'disclose', 'express', 'mention', 'reply', 'report', 'respond', 'say', 'speak', 'state', 'suggest', 'tell', 'voice' }
results = { word: defaultdict(int) for word in synonyms }

with open('../../../../tasks/02-structural-linguistics/blog2008.txt') as f:
    for i, line in enumerate(f):
        doc = nlp(line.strip())
        for token in doc:
            text, pos, dep, lemma = token.text, token.pos_, token.dep_, token.lemma_
            if pos == 'VERB' and lemma in synonyms:
                for child in token.children:
                    c_text, c_dep = child.text.lower(), child.dep_
                    if c_dep == 'advmod' and c_text.endswith('ly'):
                        results[lemma][c_text] += 1

collocations = dict()
for v_key, v_value in results.items():
    adverbs = v_value.items()
    if len(adverbs): collocations[v_key] = sorted(adverbs, reverse=True, key=lambda a: a[1])[:10]

print(collocations)
