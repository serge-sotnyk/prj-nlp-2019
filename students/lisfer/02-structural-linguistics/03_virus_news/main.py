import click
import spacy

from sys import argv


FILE_SENTI = 'SentiWordNet_3.0.0.txt'
POS_WORDNET = dict(NOUN='n', VERB='v', ADJ='a', ADV='r')


def add_senti_words(data, words, pos, positive, negative):
    for word in words.split():
        clear_word, id = word.split('#')
        values = data.get(clear_word, {})
        try:
            values[id] = pos, float(positive), float(negative)
        except Exception as e:
            print(f'"{positive}" "{negative}"', e)
        data[clear_word] = values
    return data


def load_senti():
    data = {}
    try:
        for line in open(FILE_SENTI):
            line = line.strip()
            if line.startswith('#'):
                continue
            pos, id, positive, negative, words, gloss = line.split('\t')
            data = add_senti_words(data, words, pos, positive, negative)
        return data
    except OSError as e:
        print ('An error has happened:', e)
        return {}


nlp = spacy.load('en_core_web_sm')
senti = load_senti()


def is_personal(token):
    return token.pos_ == 'PROPN' and token.ent_type_ == 'PERSON'


def is_comparison(token):
    attrs = token.vocab.morphology.tag_map[token.tag_]
    return attrs.get('Degree') in ('sup', 'comp')


def is_sentiment(token):
    if token.pos_ not in POS_WORDNET:
        return False
    senti_words = senti.get(token.lemma_)
    if not senti_words:
        return False
    rate = max([max(p, n) for pos, p, n in senti_words.values() if pos == POS_WORDNET[token.pos_]], default=0)
    return rate > 0.5


def analyze_row(sentence):
    doc = nlp(sentence)
    personal = False
    comparison = False
    sentiment = False
    for token in doc:
        personal = personal or is_personal(token)
        comparison = comparison or is_comparison(token)
        sentiment = sentiment or is_sentiment(token)
    return personal, comparison, sentiment


def main():

    if len(argv) < 2:
        print('Need to specify filename!')
        exit()

    output = [0, 0, 0]

    try:
        total_lines = sum([1 for i in open(argv[1])])
        for line in open(argv[1]):
            output = map(sum,zip(output, analyze_row(line.strip())))
        personal, comparison, sentiment = output
        print(f"Rated as personal: {personal} from {total_lines} == {personal / total_lines * 100:.2f}%")
        print(f"Rated as comparison: {comparison} from {total_lines} == {comparison / total_lines * 100:.2f}%")
        print(f"Rated as sentiment: {sentiment} from {total_lines} == {sentiment / total_lines * 100:.2f}%")
    except OSError as e:
        print ('An error has happened:', e)
    return


if __name__ == "__main__":
    main()