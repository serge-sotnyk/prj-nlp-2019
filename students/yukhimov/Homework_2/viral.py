import spacy
from nltk.corpus import sentiwordnet as swn


nlp = spacy.load('en_core_web_md')
ENTITY_LABELS = ('PERSON', 'ORG')
COMPARATIVE_SUPELATIVE_TAGS = ('JJR', 'JJS', 'RBR', 'RBS')


def find_entities(doc):
    for ent in doc.ents:
        if ent.label_ in ENTITY_LABELS:
            return True


def find_comparison(doc):
    for token in doc:
        if token.tag_ in COMPARATIVE_SUPELATIVE_TAGS:
            return True


def check_sentiment(doc):
    for token in doc:
        wn = convert_to_wn(token.tag_)
        if wn:
            synset_form = list(swn.senti_synsets(token.text, wn))
            if len(synset_form) > 5:
                synset_form = synset_form[:5]
            positive = []
            negative = []
            for form in synset_form:
                positive.append(form.pos_score())
                negative.append(form.neg_score())
            avg_positive = avg_negative = 0
            if positive:
                avg_positive = round(sum(positive) / len(positive), 1)
            if negative:
                avg_negative = round(sum(negative) / len(negative), 1)
            if avg_positive or avg_negative > 0.5:
                return True


def convert_to_wn(tag):
    if tag.startswith('J'):
        return 'a'
    elif tag.startswith('N'):
        return 'n'
    elif tag.startswith('R'):
        return 'r'
    elif tag.startswith('V'):
        return 'v'


def check_viral(filename):
    counter = 0
    entities = 0
    comparison = 0
    sentiment = 0
    with open(filename, "r") as input_file:
        for headline in input_file:
            counter += 1
            doc = nlp(headline)
            if find_entities(doc):
                entities += 1
            if find_comparison(doc):
                comparison += 1
            if check_sentiment(doc):
                sentiment += 1
    with open('viral_results.txt', "w") as output_file:
        output_file.write('Entities: {}%\n'.format(round(entities / counter * 100)))
        output_file.write('Comparison: {}%\n'.format(round(comparison / counter * 100)))
        output_file.write('Sentiment: {}%\n'.format(round(sentiment / counter * 100)))


if __name__ == "__main__":
    check_viral('examiner-headline.txt')
