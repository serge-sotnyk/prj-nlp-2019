import re
from tqdm import tqdm
from collections import Counter

import spacy
from spacy.matcher import Matcher
from spacy import displacy

text_file = '../../../tasks/02-structural-linguistics/blog2008.txt'

def get_sentence():
	with open(text_file, 'r') as f:
		for line in f:
			yield line


nlp = spacy.load('en_core_web_sm', disable=['ner'])


ly_flag = lambda text: bool(re.compile(r'[a-zA-Z]+ly').match(text))
LY_WORD = nlp.vocab.add_flag(ly_flag)

verb_pattern = lambda verb: [{'LEMMA': verb, 'POS': 'VERB'}, {'POS': 'ADV', LY_WORD: True}]


matcher = Matcher(nlp.vocab)

verbs = ['say', 'tell', 'speak', 'claim', 'communicate']
for verb in verbs:
	matcher.add(verb.upper(), None, verb_pattern(verb))

if __name__ == '__main__':
	text = get_sentence()
	for s in tqdm(text):
		doc = nlp(s)
		matches = matcher(doc)
		# if matches:
		# 	for token in doc:
		# 		print('{:>20} {:>10} {:>10} {:>10}'.format(token.text, token.pos_, token.dep_, token.head.text))
		for match_id, start, end in matches:
			string_id = nlp.vocab.strings[match_id]
			span = doc[start: end]
			print(match_id, string_id, start, end, span.text)