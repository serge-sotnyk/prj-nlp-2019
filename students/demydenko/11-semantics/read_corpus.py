#%%
from __future__ import absolute_import, division, print_function
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
# gensim    
import gensim
from gensim.models import KeyedVectors

from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
#%%
def split_tags(string):
    return [tuple(i.split("/")) for i in string.split()]

def readTrainData(filename):
    data = []
    for line in open(filename):
        line = line.strip()
        #read in training or dev data with labels
        if len(line.split('\t')) == 7:
            (trendid, trendname, origsent, candsent, judge, origsenttag, candsenttag) = \
            line.split('\t')
        else:
            continue
        # ignoring the training data that has middle label 
        nYes = eval(judge)[0]            
        if nYes >= 3:
            amt_label = True
            data.append((split_tags(origsenttag), split_tags(candsenttag), amt_label))
        elif nYes <= 1:
            amt_label = False
            data.append((split_tags(origsenttag), split_tags(candsenttag), amt_label))
    return data

def readTestData(filename):
    data = []
    for line in open(filename):
        line = line.strip()
        #read in training or dev data with labels
        if len(line.split('\t')) == 7:
            (trendid, trendname, origsent, candsent, judge, origsenttag, candsenttag) = \
            line.split('\t')
        else:
            continue
        # ignoring the training data that has middle label 
        nYes = int(judge[0])
        if nYes >= 4:
            expert_label = True
        elif nYes <= 2:
            expert_label = False
        else:
            expert_label = None
        data.append((split_tags(origsenttag), split_tags(candsenttag), expert_label))
    return data
#%%
train_data = readTrainData("data/dev.data")
test_data = readTestData("data/test.data")
# %%
print('loading word vectors')
word_vectors = KeyedVectors.load_word2vec_format("vectors/numberbatch-en-17.06.txt.gz", binary=False)
print('loading word vectors finished')
#%%
# genete input
# TODO filter stopwords

def extract_features_and_labels(data_,skip_none):
    x_data = []
    y_data = []
    i=-1
    for case in data_:
        i=i+1
        # first_sentence = " ".join([t[0].lower() for t in case[0]])
        # second_sentence = " ".join([t[0].lower() for t in case[1]])
        first_set_of_tokens = [t[0].lower() for t in case[0] if t[0].lower() not in set(stopwords.words('english')) ]
        second_set_of_tokens = [t[0].lower() for t in case[1] if t[0].lower() not in set(stopwords.words('english')) ]
        f = first_set_of_tokens
        s = second_set_of_tokens
        # ця фіча погіршувала картину
        # inter = len(set(s).intersection(set(f)))/(len(f)+len(s))
        # skip vector not in vocabulary
        first_set_of_tokens = [t for t in first_set_of_tokens if t in  word_vectors.vocab]
        second_set_of_tokens = [t for t in second_set_of_tokens if t in  word_vectors.vocab]
        if len(first_set_of_tokens)==0 or len(second_set_of_tokens)==0:
            n_sim = 100
            similarity = 100
        else:
            n_sim = word_vectors.n_similarity(first_set_of_tokens, second_set_of_tokens)
            first_sentence = " ".join([t[0].lower() for t in case[0] if t[0].lower() not in set(stopwords.words('english')) ])
            second_sentence = " ".join([t[0].lower()  for t in case[1] if t[0].lower() not in set(stopwords.words('english')) ])
            similarity = word_vectors.wmdistance(first_sentence, second_sentence)

        if (case[2]!=None):
            # x_data.append([n_sim, similarity])
            x_data.append([n_sim, similarity])
            y_data.append(str(case[2]).lower())
        else:
            if not skip_none:
                x_data.append([n_sim, similarity])
                y_data.append('----')
            pass
            
    return x_data, y_data

# x_train , y_train = extract_features_and_labels(train_data,skip_none=True)
x_train , y_train = extract_features_and_labels(train_data, skip_none=False)
x_test , y_test = extract_features_and_labels(test_data, skip_none=False)
# for case in test_data:
#     i=i+1
#     first_sentence = " ".join([t[0].lower() if t[0].lower() not in set(stopwords.words('english')) else ' ' for t in case[0]])
#     second_sentence = " ".join([t[0].lower() if t[0].lower() not in set(stopwords.words('english')) else ' ' for t in case[1]])
#     similarity = word_vectors.wmdistance(first_sentence, second_sentence)
#     if (case[2]!=None):
#         x_test.append(similarity)
#         # y_test.append(case[2])
#         y_test.append(str(case[2]).lower())
#     else:
#         pass
#%%
# x_train = np.array(x_train).reshape(-1, 1)
# x_test = np.array(x_test).reshape(-1, 1)

clf = LogisticRegression(random_state=1)
# clf = LinearSVC(random_state=0)

clf.fit(x_train, y_train)
predictions = clf.predict(x_test)

print(classification_report(y_test, predictions))
print("Accuracy:", accuracy_score(y_test, predictions))

# output without probability
f = open("PIT2015_BASELINE_SIM_SEM.output","w")
for t in predictions:
    if t:
        f.write("{}	0.0000\n".format(str(t).lower()))
    else:
        f.write("{}	0.0000\n".format(str(t).lower()))
f.close()
#%%

predictions_proba = clf.predict_proba(x_test)
clf.score(x_test, y_test)
# output with probability
f = open("PIT2015_BASELINE_SIM_SEM.output","w")
for t in predictions_proba:
    
    if t[0]>t[1]: 
        f.write("{}	{:.4f}\n".format('false', 1-t[0])) # схоже все що менше 0.5 вважається як false/ 
    else:
        f.write("{}	{:.4f}\n".format('true', t[1]))
f.close()

# print(classification_report(y_test, predictions))
# print("Accuracy:", accuracy_score(y_test, predictions))
# precision    recall  f1-score   support

#        False       0.83      0.95      0.89       663
#         True       0.61      0.29      0.39       175

#     accuracy                           0.81       838
#    macro avg       0.72      0.62      0.64       838
# weighted avg       0.79      0.81      0.78       838

# Accuracy: 0.8126491646778043

# without stopwords
# precision    recall  f1-score   support

#        False       0.85      0.94      0.89       663
#         True       0.62      0.37      0.46       175

#     accuracy                           0.82       838
#    macro avg       0.74      0.65      0.68       838
# weighted avg       0.80      0.82      0.80       838

# Accuracy: 0.8210023866348448


# АЛЕ!!!
# python3 scripts/pit2015_eval_single.py data/test.label systemoutputs/PIT2015_BASELINE_SIM_SEM.output
# 838	BASELINE	SIM_SEM		F: 0.460	Prec: 0.621	Rec: 0.366		P-corr: 0.405	F1: 0.493	Prec: 0.474	Rec: 0.514
# розібрався, за оцінку береться найгірший клас, дійсно якщо глянути в таблицю вище:

#                 precision    recall  f1-score   support
#         True       0.62      0.37      0.46       175

# вивід із ймоіврносями впливає тільки на другу частину оцінки(P-corr: 0.405	F1: 0.493	Prec: 0.474	Rec: 0.514)

# додав нову фічу
# precision    recall  f1-score   support

#         ----       0.00      0.00      0.00       134
#        false       0.78      0.93      0.84       663
#         true       0.55      0.56      0.55       175

#     accuracy                           0.73       972
#    macro avg       0.44      0.50      0.47       972
# weighted avg       0.63      0.73      0.68       972

# python3 scripts/pit2015_eval_single.py data/test.label PIT2015_BASELINE_SIM_SEM.output 
# 838     BASELINE        SIM_SEM         F: 0.611        Prec: 0.671     Rec: 0.560              P-corr: 0.536   F1: 0.621       Prec: 0.624     Rec: 0.617