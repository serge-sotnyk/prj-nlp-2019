import datetime
import json

import spacy


print('Started {}'.format(datetime.datetime.now()))

nlp = spacy.load('en_core_web_lg')

input_file = '../../../tasks/02-structural-linguistics/blog2008.txt'

verbs = ["say", "tell", "speak", "claim", "communicate", "declare", "mention", "shout", "suggest"]


results_dict = dict()
for v in verbs:
    results_dict[v] = dict()


def process_line(line: str):
    doc = nlp(line)
    for token in doc:
        if token.pos_ == 'VERB' and token.lemma_ in verbs:
            key = token.lemma_
            for child in token.children:
                if child.pos_ == 'ADV' and str(child).endswith('ly'):
                    child = str(child).lower()
                    if child in results_dict[key].keys():
                        results_dict[key][child] += 1
                    else:
                        results_dict[key][child] = 1


with open(input_file) as f:
    lines = [line.rstrip('\n') for line in f]
    for l in lines:
        process_line(l)


for r in results_dict:
    inner_dict = results_dict[r].items()
    sorted_dict = sorted(inner_dict, key=lambda kv: kv[1], reverse=True)
    results_dict[r] = sorted_dict[:10]
    print(results_dict[r])

saved = json.dumps(results_dict, ensure_ascii=False, indent=4)
print(saved)
print('Finished {}'.format(datetime.datetime.now()))

