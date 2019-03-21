import spacy
from nltk.corpus import sentiwordnet as swn

nlp = spacy.load('en_core_web_lg')

entities = 0
emotional = 0
qualitative = 0

viral_entities = { 'PERSON', 'NORP', 'EVENT', 'ORG' }
qualitative_tags = { 'RBR', 'RBS', 'JJR', 'JJS' }

nouns = { 'NN', 'NNP', 'NNPS', 'NNS' }
verbs = { 'BES', 'HVS', 'MD', 'VB', 'VBD', 'VBZ', 'VBG', 'VBN', 'VBP' }
adjectives = { 'JJ', 'JJR', 'JJS' }
adverbs = { 'RB', 'RBR', 'RBS', 'RP', 'WRB' }

S_LIMIT = 4
EMOTIONAL_THRESHOLD = 0.65

def get_swn_pos(tag: str):
    if tag in nouns:
        return 'n'
    elif tag in verbs:
        return 'v'
    elif tag in adjectives:
        return 'a'
    elif tag in adverbs:
        return 'r'
    return None

with open('../../../../tasks/02-structural-linguistics/examiner-headlines.txt') as f:
    for headline in f:
        doc = nlp(headline)
        entity_found = False
        qualitative_found = False
        h_positive = []
        h_negative = []

        for token in doc:
            swn_pos = get_swn_pos(token.tag_)
            if swn_pos:
                try:
                    t_positive = []
                    t_negative = []
                    for i, s in enumerate(swn.senti_synsets(token.text, swn_pos)):
                        pos_score, neg_score = s.pos_score(), s.neg_score()
                        if pos_score: t_positive.append(pos_score)
                        if neg_score: t_negative.append(neg_score)
                        if i == S_LIMIT:
                            break
                    if len(t_positive): h_positive.append(sum(t_positive)/len(t_positive))
                    if len(t_negative): h_negative.append(sum(t_negative)/len(t_negative))
                except:
                    pass
        
            if not entity_found and token.ent_type_ in viral_entities:
                entities += 1
                entity_found = True
            if not qualitative_found and token.tag_ in qualitative_tags:
                qualitative += 1
                qualitative_found = True

        h_positive_sum = sum(h_positive)/len(h_positive) if len(h_positive) else 0
        h_negative_sum = sum(h_negative)/len(h_negative) if len(h_negative) else 0

        if h_positive_sum >= EMOTIONAL_THRESHOLD or h_negative_sum >= EMOTIONAL_THRESHOLD: 
            emotional += 1

