from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.externals import joblib

from conllu_utils import load_trees, TRAIN_FILENAME, extract_features_and_y, TEST_FILENAME


def extract_x_y(name: str):
    trees = load_trees(name)
    x, y = [], []
    for tree in trees:
        xs, ys = extract_features_and_y(tree)
        x += xs
        y += ys
    return x, y


def store_weak_model(classifier, vectorizer):
    joblib.dump(classifier, "data/weak_classifier.sav")
    joblib.dump(vectorizer, "data/weak_vectorizer.sav")


def load_weak_model():
    classifier = joblib.load("data/weak_classifier.sav")
    vectorizer = joblib.load("data/weak_vectorizer.sav")
    return classifier, vectorizer


def main():
    x_train, y_train = extract_x_y(TRAIN_FILENAME)
    vectorizer = DictVectorizer()
    vec = vectorizer.fit(x_train)
    print("\nTotal number of features: ", len(vec.get_feature_names()))

    x_train_vectorized = vec.transform(x_train)

    x_test, y_test = extract_x_y(TEST_FILENAME)
    x_test_vectorized = vec.transform(x_test)

    classifier = LogisticRegression(random_state=1974, solver="sag", max_iter=10000, verbose=1)
    classifier.fit(x_train_vectorized, y_train)

    predicted = classifier.predict(x_test_vectorized)
    print(classification_report(y_test, predicted))

    store_weak_model(classifier, vectorizer)


if __name__ == "__main__":
    main()
