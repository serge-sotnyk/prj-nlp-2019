import spacy

nlp = spacy.load('en_core_web_md')
VERBS = ('say', 'tell', 'speak', 'claim', 'communicate', 'articulate', 'enunciate', 'state', 'talk', 'utter',
         'verbalize', 'vocalize', 'declare', 'transmit')


def find_collocations(text, results):
    doc = nlp(text)
    tagged_verbs = [(token.lemma_, token.children) for token in doc if token.pos_ == 'VERB' and token.lemma_ in VERBS]
    for verb, children in tagged_verbs:
        for word in children:
            if word.pos_ == 'ADV' and word.text.endswith('ly'):
                adverb = word.text.lower()
                if adverb in results[verb].keys():
                    results[verb][adverb] += 1
                else:
                    results[verb][adverb] = 1


def sort_dict(results):
    with open('collocations_results.txt', "w") as output_file:
        for verb, adverbs in results.items():
            sorted_adverbs = sorted(adverbs.items(), key=lambda value: value[1], reverse=True)
            output_file.write('{}: {}\n'.format(verb, sorted_adverbs))


def process_file(filename):
    results = {}
    for verb in VERBS:
        results[verb] = {}
    with open(filename, "r") as input_file:
        for line in input_file:
            find_collocations(line, results)
    sort_dict(results)


if __name__ == "__main__":
    process_file('blog2008.txt')
