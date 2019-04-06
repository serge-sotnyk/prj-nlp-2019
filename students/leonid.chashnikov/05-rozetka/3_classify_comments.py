import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import Perceptron
from sklearn.model_selection import ShuffleSplit, cross_validate
from sklearn.naive_bayes import GaussianNB


def _read_comments():
    with open('./processed_comments.p', 'rb') as f:
        result = pickle.load(f)
    return result


if __name__ == "__main__":
    comments = _read_comments()
    print(len(comments))
    features = [c['text'] for c in comments]
    target = [c['label'] for c in comments]

    count_vect = CountVectorizer()
    features_vector = count_vect.fit_transform(features)
    print(features_vector.shape)

    split = ShuffleSplit(test_size=0.3, train_size=0.7, random_state=42)
    scoring = ['precision_macro', 'recall_macro']

    clf_nb = GaussianNB()
    scores = cross_validate(clf_nb, features_vector.toarray(), target, scoring=scoring, cv=split)
    print('GaussianNB:\n\tprecision {}, recall {}'
          .format(scores['test_precision_macro'].mean(), scores['test_recall_macro'].mean()))

    clf_per = Perceptron()
    scores = cross_validate(clf_per, features_vector.toarray(), target, scoring=scoring, cv=split)
    print('Perceptron:\n\tprecision {}, recall {}'
          .format(scores['test_precision_macro'].mean(), scores['test_recall_macro'].mean()))

