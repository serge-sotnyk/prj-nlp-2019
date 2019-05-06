from gensim.models import KeyedVectors
import json
import random
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import numpy
import re

with open('request_messages.txt') as json_file:
    data = json.load(json_file)

messages = data['messages']
random.shuffle(messages)

train_set, test_set = messages[:43205], messages[43205:]

train_messages = [item['message'] for item in train_set]
train_labels = [item['category'] for item in train_set]
test_messages = [item['message'] for item in test_set]
test_labels = [item['category'] for item in test_set]

uk_vectors = KeyedVectors.load_word2vec_format('news.lowercased.tokenized.word2vec.300d', binary=False)


def vectorize_message(message):
    message_vector = []
    words = message.split()
    for word in words:
        word = re.sub(r'[^\w]', '', word)
        try:
            message_vector.append(uk_vectors.get_vector(word).tolist())
        except KeyError:
            pass
    if not message_vector:
        return numpy.array([0] * 300)
    message_vector = numpy.array(message_vector)
    return numpy.sum(message_vector, axis=0)


train_features = numpy.array([vectorize_message(message) for message in train_messages])
test_features = numpy.array([vectorize_message(message) for message in test_messages])

knn = KNeighborsClassifier(n_neighbors=5)

knn.fit(train_features, train_labels)
y_pred = knn.predict(test_features)

print("Accuracy:", metrics.accuracy_score(test_labels, y_pred))
print(metrics.classification_report(test_labels, y_pred))


'''
Baseline


Accuracy: 0.3149168286887017

            precision    recall  f1-score   support

micro avg       0.31      0.31      0.31     18516
macro avg       0.25      0.16      0.17     18516
weighted avg    0.32      0.31      0.29     18516


'''