import spacy
from nltk.corpus import sentiwordnet as swn


nlp = spacy.load('en_core_web_lg')

input_file = '../../../tasks/02-structural-linguistics/examiner-headlines.txt'
NAMED_ENTITY_TYPES = ['PERSON', 'NORP', 'ORG', 'PRODUCT', 'EVENT', 'MONEY', 'LAW']


class Score:
    doc_count = 0
    emotional_count = 0
    comp_sup_count = 0
    ner_count = 0


# try with whole string
def is_emotional(word: str):
    senti_scores_list = list(swn.senti_synsets(word))[:5]
    positive_scores = [w.pos_score() for w in senti_scores_list if w.pos_score() != 0.0]
    negative_scores = [w.neg_score() for w in senti_scores_list if w.neg_score() != 0.0]
    positive_avg = sum(positive_scores) / len(positive_scores) if len(positive_scores) != 0 else 0
    negative_avg = sum(negative_scores) / len(negative_scores) if len(negative_scores) != 0 else 0
    return positive_avg > 0.5 or negative_avg > 0.5


def has_ne(entities):
    return any(e.label_ in NAMED_ENTITY_TYPES for e in entities)


def process_line(line: str, score: Score):
    doc = nlp(line)
    score.doc_count += 1

    has_named_entities = has_ne(doc.ents)

    comparative_superlative = False
    emotional = False
    for token in doc:

        token_str = str(token).lower()
        if is_emotional(token_str):
            emotional = True

        # has comparative or superlative JJs or RBs
        if token.tag_ in ['JJR', 'JJS', 'RBR', 'RBS']:
            comparative_superlative = True

    if has_named_entities:
        score.ner_count += 1
    if emotional:
        score.emotional_count += 1
    if comparative_superlative:
        score.comp_sup_count += 1

    pass


with open(input_file) as f:
    lines = [line.rstrip('\n') for line in f]
    current_score = Score()
    for l in lines:
        process_line(l, current_score)

    print('Doc count: {}'.format(current_score.doc_count))
    print('Named Entities: {}'.format(current_score.ner_count))
    print('Emotional: {}'.format(current_score.emotional_count))
    print('Comparative/Superlative: {}'.format(current_score.comp_sup_count))

