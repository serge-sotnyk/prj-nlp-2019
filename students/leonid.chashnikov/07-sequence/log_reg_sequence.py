import json

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
import baseline_solution
from sklearn.metrics import classification_report


def _get_feature_dict(token, prev_token, next_token):
    result_dict = dict()
    result_dict['word'] = token.lower()
    result_dict['is_capitalized'] = token.istitle()
    result_dict['is_not_punct'] = token.isalnum()
    result_dict['is_uppercase'] = token.isupper()

    # result_dict['is_ner'] = token.isupper()  #change to spacy
    # result_dict['pos'] = str(morph.tag(token)[0].POS)  #change to spacy
    # result_dict['word_lemma'] = morph.normal_forms(token)[0]   #change to spacy

    if prev_token:
        result_dict['prev_word'] = prev_token.lower()
        # result_dict['prev_pos'] = str(morph.tag(prev_token)[0].POS)
    else:
        result_dict['prev_word'] = ''
        result_dict['prev_pos'] = 'None'

    if next_token:
        result_dict['next_word'] = next_token.lower()
        # result_dict['next_pos'] = str(morph.tag(prev_token)[0].POS)
    else:
        result_dict['next_word'] = ''
        result_dict['next_pos'] = 'None'
    return result_dict


def _get_features(tokens: list):
    features = []
    for index in range(len(tokens)):
        token = tokens[index]
        prev_token = tokens[index-1] if index > 0 else None
        next_token = tokens[index+1] if index < len(tokens) - 1 else None
        result_dict = _get_feature_dict(token, prev_token, next_token)
        features.append(result_dict)
    return features


def _read_test_data():
    with open('../../../tasks/07-language-as-sequence/run-on-test.json', 'r') as f:
        data = json.load(f)
    return data


def _corpus_to_list(sents):
    return [' '.join(sent) for sent in sents if len(sent) > 3]


def _filter_out_stop_sign(sent):
    if sent[-1] == '.' or sent[-1] == '?' or sent[-1] == '!':  # todo maybe there's full list somewhere
        return sent[:-1]
    else:
        return sent


def _transform_test_data(test_data):
    raw_tokens = []
    labels = []
    for sentence in test_data:
        for token in sentence:
            raw_tokens.append(token[0])
            labels.append(token[1])
    return raw_tokens, labels


def _flatten(l):
    flat_list = [item for sublist in l for item in sublist]
    return flat_list


def _merge_sentences_by_two_and_tag(sents):
    raw_tokens = []
    labels = []
    # for index in range(start=0, stop=len(sents) - 1, step=2):
    for index in range(len(sents) - 1):
        sent_1 = sents[index].split()
        sent_2 = sents[index + 1].split()
        sent_1 = _filter_out_stop_sign(sent_1)
        merged = sent_1 + sent_2
        raw_tokens.append(merged)

        sent_label = [False] * len(merged)
        sent_label[len(sent_1) - 1] = True
        labels.append(sent_label)

    raw_tokens = _flatten(raw_tokens)
    labels = _flatten(labels)
    return raw_tokens, labels


def _download_train():
    # import nltk
    # nltk.download('treebank')
    # nltk.download('inaugural')
    # nltk.download('brown')
    # nltk.download('punkt')
    # nltk.download('twitter_samples')
    # nltk.download('gutenberg')

    from nltk.corpus import inaugural
    from nltk.corpus import treebank
    from nltk.corpus import brown
    from nltk.corpus import gutenberg

    # inaugural_sents = _corpus_to_list(inaugural.sents())
    brown_sents = _corpus_to_list(brown.sents())  # looks ok, but needs cleaning from special symbols
    ptb_sents = list()  # _corpus_to_list(treebank.sents()) - not raw sentences :( needs cleaning from special symbols and tags
    gutenberg_sents = list()  # _corpus_to_list(gutenberg.sents())
    # print('Inaugural {}'.format(len(inaugural.sents())))
    # print('Brown {}'.format(len(brown.sents())))
    # print('Gutenberg {}'.format(len(gutenberg.sents())))

    return brown_sents + ptb_sents + gutenberg_sents


if __name__ == "__main__":
    # Baseline
    test_data = _read_test_data()
    baseline_solution.evaluate_baseline(test_data)

    # Test data
    test_raw_tokens, test_labels = _transform_test_data(test_data)
    test_features = _get_features(test_raw_tokens)
    print('Test features {}, test labels {}'.format(len(test_features), len(test_labels)))

    # Train data
    train_data = _download_train()
    raw_train_tokens, train_labels = _merge_sentences_by_two_and_tag(train_data)
    train_features = _get_features(raw_train_tokens)

    # DictVectorizer
    dict_vect = DictVectorizer()
    train_features = dict_vect.fit_transform(train_features)
    test_features = dict_vect.transform(test_features)

    # LogisticRegression
    clf_lr = LogisticRegression(random_state=42, solver="sag")
    clf_lr.fit(train_features, train_labels)
    predicted_labels = clf_lr.predict(test_features)
    scores = classification_report(test_labels, predicted_labels)

    print(scores)
