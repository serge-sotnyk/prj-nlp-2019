from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from nltk import download
import numpy
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from keras.models import Sequential
from keras.layers import Dense

with open('data/train.data', 'r') as input_file:
    train_data = input_file.readlines()

with open('data/test.data', 'r') as input_file:
    test_data = input_file.readlines()


train_tweets = []
train_labels = []

for line in train_data:
    columns = line.split('\t')
    if columns[4] != '(2, 3)':
        train_tweets.append((columns[2], columns[3]))
        if columns[4] in ('(1, 4)', '(0, 5)'):
            train_labels.append(0)
        else:
            train_labels.append(1)

test_tweets = []
test_labels = []

for line in test_data:
    columns = line.split('\t')
    if columns[4] != '3':
        test_tweets.append((columns[2], columns[3]))
        if columns[4] in ('4', '5'):
            test_labels.append(1)
        else:
            test_labels.append(0)


model = KeyedVectors.load_word2vec_format('numberbatch-en.txt', binary=False)

download('stopwords')
stop_words = stopwords.words('english')


def get_wmdistance(train_tweets):
    distance_array = []
    for tweets in train_tweets:
        tweet_1 = [word for word in tweets[0].lower().split() if word not in stop_words]
        tweet_2 = [word for word in tweets[1].lower().split() if word not in stop_words]
        distance_array.append([model.wmdistance(tweet_1, tweet_2)])
    return numpy.array(distance_array)


train_features = get_wmdistance(train_tweets)
test_features = get_wmdistance(test_tweets)

train_features = numpy.ma.masked_array(train_features, ~numpy.isfinite(train_features)).filled(0)
test_features = numpy.ma.masked_array(test_features, ~numpy.isfinite(test_features)).filled(0)

logreg = LogisticRegression()

logreg.fit(train_features, train_labels)
y_pred = logreg.predict(test_features)

print("Accuracy:", metrics.accuracy_score(test_labels, y_pred))
print(metrics.classification_report(test_labels, y_pred))


nn_model = Sequential()
nn_model.add(Dense(32, input_dim=1, activation='relu'))
nn_model.add(Dense(16, activation='relu'))
nn_model.add(Dense(1, activation='sigmoid'))

nn_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

nn_model.fit(train_features, train_labels, epochs=150, batch_size=10)

score = nn_model.evaluate(test_features, test_labels)

print("Accuracy: {}".format(score[1]))


'''
Logistic Regression

Accuracy: 0.8389021479713604
              precision    recall  f1-score   support

           0       0.87      0.93      0.90       663
           1       0.66      0.48      0.55       175

   micro avg       0.84      0.84      0.84       838
   macro avg       0.76      0.71      0.73       838
weighted avg       0.83      0.84      0.83       838


NN

Accuracy: 0.834128878281623
'''