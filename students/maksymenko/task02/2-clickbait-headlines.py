from nltk.corpus import sentiwordnet as swn
import nltk
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
import en_core_web_md

nlp = en_core_web_md.load()

# nltk.download('wordnet')
# nltk.download('sentiwordnet')
# nltk.download('stopwords')

INPUT_FILE = 'tasks/02-structural-linguistics/examiner-headlines.txt'

class ClickbaitHeadlineRecognizer():

    def __init__(self, headline):
        self.headline = headline

    def has_ne(self, token):
        return bool(token.ent_type_)

    def has_comp_or_sup(self, token):
        return token.tag_ in ['JJR', 'JJS', 'RBR', 'RBS']

    def get_swn_pos(self, pos):
        map_pos_to_swn_pos = {
            'VERB': 'v',
            'NOUN': 'n',
            'PROPN': 'n',
            'ADJ': 'a',
            'ADV': 'r',
        }
        try:
            return map_pos_to_swn_pos[pos]
        except:
            return 'a'

    def evaluate_headline(self):
        line = nlp(self.headline)

        if len(line) == 0:
            return False

        score_sum = 0
        token_count = 1
        has_ne = False
        has_comp_or_sup = False

        for token in line:
            token_score = self.is_token_emotional(token)
            if self.has_ne(token):
                has_ne = True

            if self.has_comp_or_sup(token):
                has_comp_or_sup = True

            if token_score is not None:
                token_count += 1
                if token_score:
                    score_sum += 1
        score_mean = score_sum / token_count

        is_emotional = score_mean > 0.2

        if is_emotional:
            print(score_mean, self.headline)

        return {'is_emotional': is_emotional, 'has_ne': has_ne, 'has_comp_or_sup': has_comp_or_sup}

    def get_synsets(self, token):
        stopwords = nltk.corpus.stopwords.words('english')
        lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
        stop_poss = ['PUNCT', 'X', 'SYM', 'CONJ', 'ADP', 'PART', 'SPACE', 'INTJ']

        if token.text in stopwords or token.pos_ in stop_poss:
            return []

        swn_pos = self.get_swn_pos(token.pos_)
        lemma = lemmatizer(token.text, token.pos_)

        return list(swn.senti_synsets(lemma[0], pos=swn_pos))[:5]
        # return list(swn.senti_synsets(token.text, pos=swn_pos))[:5]

    def is_token_emotional(self, token):
        synset = self.get_synsets(token)
        synset_len = len(synset)

        if synset_len == 0:
            return None

        token_neg_sum = 0
        token_pos_sum = 0

        for s in synset:
            token_neg_sum += s.neg_score()
            token_pos_sum += s.pos_score()

        token_neg_score = token_neg_sum / synset_len
        token_pos_score = token_pos_sum / synset_len

        return token_neg_score > 0.5 or token_pos_score > 0.5


# headline1 = 'Rescued Blind Dog Looking for Her Seeing Eye Person/Guide Person'
# recognizer = ClickbaitHeadlineRecognizer(headline1)

is_emotional_count = 0
has_ne_count = 0
has_comp_or_sup_count = 0

with open(INPUT_FILE, 'r', encoding='utf-8') as input_file:
    lines_count = 0
    for line in input_file:
        lines_count += 1
        recognizer = ClickbaitHeadlineRecognizer(line)
        scores = recognizer.evaluate_headline()

        if scores['is_emotional']:
            is_emotional_count += 1

        if scores['has_ne']:
            has_ne_count += 1

        if scores['has_comp_or_sup']:
            has_comp_or_sup_count += 1

    print(f'There are {is_emotional_count / lines_count * 100}% emotional headlines')
    print(f'{has_ne_count / lines_count * 100}% headlines have named entities')
    print(f'{has_comp_or_sup_count / lines_count * 100}% headlines have comparative or superlative ADV or ADJ')

# Чи є в заголовку іменовані стуності? - 80,32%
# Чи є заголовок позитивно чи негативно забарвлений? - 1,52%
# Чи є в заголовку прикметники та прислівники вищого і найвищого ступенів порівняння? - 4,64%

