import spacy

from datetime import datetime
from collections import Counter, defaultdict
from sys import argv


FIRST_N = 10
synonyms = [
    "advice", "announce", "chat", "claim", "collogue", "communicate", "confab", "converse", "convey", 
    "explain", "express", "gossip", "inform", "instruct", "narrate", "notify", "parley", "point", "recite", "reckon", 
    "refer", "report", "say", "speak", "talk", "tell", "utter", "verbalize", "voice", "whisper"]
nlp = spacy.load('en_core_web_sm')


def procceed(data, line):
    doc = nlp(line)
    for token in doc:
        if token.pos_ == 'VERB' and token.lemma_ in synonyms:
            for child in token.children:
                if child.pos_ == 'ADV' and child.lemma_.endswith('ly'):
                    data[token.lemma_][child.lemma_] = data[token.lemma_].get(child.lemma_, 0) + 1
    return data


def pprint(data):
    if not data:
        return
    print('---------')
    for verb in sorted(data):
        print (verb, data[verb].most_common(FIRST_N))


def main(income_file, buf_size=70):
    data = defaultdict(Counter)
    buf = []
    try:
        total_lines = sum([1 for i in open(income_file)])
        print('Total lines:', total_lines)
        for n, line in enumerate(open(income_file)):
            buf.append(line)
            if len(buf) == buf_size:
                data.update(procceed(data, ' '.join(buf)))
                buf = []
            if n and n % 1000 == 0:
                print (n, 'from', total_lines)
        if buf:
            data.update(procceed(data, ' '.join(buf)))
    except OSError as e:
        return print('Failed to open file', income_file, e)        
    
    return data


if __name__ == "__main__":
    if len(argv) < 2:
        print('Need to specify filename!')
        exit()
    start = datetime.now()
    pprint(main(argv[1]))
    print('Program was running', datetime.now() - start)