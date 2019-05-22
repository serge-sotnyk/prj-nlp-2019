

# ------------------------------------------------------------------------
# пробував різні фічі, методи найкращий результат на 20000 тис документах.
#        accuracy                           0.84      5997
#       macro avg       0.82      0.67      0.72      5997
#    weighted avg       0.84      0.84      0.83      5997
# Test accuracy: 0.83558446
# ------------------------------------------------------------------------

# %%

import tensorflow as tf
from tensorflow import keras
# gensim
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

# load trees
import tokenize_uk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
# Helper libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score
from os import listdir
from os.path import isfile, join
from langdetect import detect
from sklearn.metrics import confusion_matrix
# import pymorphy2
import time
print(tf.__version__)

#%%
print('loading vectors')
vector_model = KeyedVectors.load_word2vec_format('/home/ds/PycharmProjects/gensim/data/ua_vec/data', binary=False)
print('vectors loaded')
# %%
'''
loading data
'''
# зберіг в pickle і закоментував
# print('loading data')
# PATH = '/home/ds/projects/nlp/data/1551'
# raw_data=[]
# onlyfiles = [f for f in listdir(PATH) if isfile(join(PATH, f))]
# for f in onlyfiles:
#     with open(PATH+'/'+f, "r") as file_to_read:
#         text = file_to_read.read()
#         raw_data.append((f.rstrip(".txt"),text))
# data=[]
# i=0
# for d in raw_data:
#     i=i+1
#     print(i)
#     parts = d[1].split('\n\n\n')
#     for p in parts:
#         id_ = str(p).split('\n')[0]
#         text = str(p)
#         if id_ in text:# %%
#             text = text.replace(id_,'')
#             if str(id_).isdigit and len(text)>10:
#                 try:
#                     if detect(text)=='uk':
#                         data.append((d[0], id_, text))
#                 except:
#                     # print(d[0], text)
#                     pass
                
#                 # else:
#                     # print(text[:10])
#         else:
#             print(id_, text)
# print('data loaded and parsed')

# saving data to pickle
# with open('data.pickle', 'wb') as f:
#      pickle.dump(data, f)
# loadind data     
with open('/home/ds/projects/nlp/prj-nlp-2019/students/demydenko/9-10_1551_nn/data.pickle', 'rb') as f:
     data_new = pickle.load(f)
data = data_new

#%%
'''
підготовка даних
'''
# використання лем не дало суттєво покращення у поточному варіанті векторів
# morph = pymorphy2.MorphAnalyzer(lang='uk')
# morph = pymorphy2.MorphAnalyzer(lang='uk',path='/home/ds/projects/tf_1/venv3/lib/python3.6/site-packages/pymorphy2_dicts_uk/data')

# для фільтрації стоп слів
with open('/home/ds/projects/nlp/prj-nlp-2019/students/demydenko/9-10_1551_nn/stopword.txt', "r") as file_to_read:
        stopwords = file_to_read.read().split('\n')

data_res=[]
# беремо лише частину даних, наприклад 4000, не вистачає потужності ноутбука
# for d in data:
for d in data[:30000]:
    i = 0
    result_vector = np.zeros(300)
    
    words_in_doc = []# TODO try set

    for t in tokenize_uk.tokenize_uk.tokenize_words(d[2]):
        # m = morph.parse(str(t).lower())[0].normal_form
        m = str(t).lower()
        category = d[0]
        
        try:
            if m in vector_model.vocab:
                
                vector = vector_model.get_vector(m)
                if (m not in stopwords) and (not m.strip().isdigit()) and len(m)>1:
                    words_in_doc.append(m)
                    # print(str(t).lower())
                    result_vector = result_vector + vector
                    i=i+1
        except:
            # print('problem for - ',t)
            
            pass
    if i > 0:
        result_vector = result_vector / i
        data_res.append([result_vector, words_in_doc, category])
    else:
        # фільтруєтся незначна кількість документів де замість пробілу використаний `-`
        print(d)
        
# отримали попередні дані у форматі 
x = [[d[0],d[1],d[2]] for d in data_res]
# d[0] - вектор нормована сума всіх векторів слів документу
# d[1] - фільтрований список слів документу
# d[2] - категорія ( для зручності, далі прибираємо)

y = [d[2] for d in data_res]
# розбиваємо на тест трейн, stratify=y! 
x_train_raw, x_test_raw, y_train_raw, y_test_raw = train_test_split(x, y, test_size=0.3, random_state=3, stratify=y)

# translate labels to indices
labels = list(set(y_train_raw + y_test_raw))
final_labels = {}
i = 0
for l in labels:
    if l not in final_labels:
        i=i+1
        final_labels[l] = i
y_train = []
y_test = []
for l in y_train_raw:
    y_train.append(final_labels[l])

for l in y_test_raw:
    y_test.append(final_labels[l])
#%%
'''
Випадок коли використовуємо лише одну фічу - нормована сума всіх векторів слів документу
'''
x_train = []
x_test = []
for d in x_train_raw: 
    x_train.append(d[0])
for d in x_test_raw:
    x_test.append(d[0])

# clf = KNeighborsClassifier(n_neighbors=3)
clf = LogisticRegression(random_state=1)
clf.fit(x_train, y_train) 
predictions = clf.predict(x_test)

target_names = [k[:15] for k in final_labels] #для зручності відображення 
print(classification_report(y_test,  predictions, target_names=target_names))

print("Accuracy:", accuracy_score(y_test, predictions))
# якщо використати KNeighborsClassifier  на 4000 документах
#        accuracy                           0.64      1200
#       macro avg       0.56      0.50      0.50      1200
#    weighted avg       0.64      0.64      0.62      1200
# Accuracy: 0.6441666666666667

# для LogisticRegression на 4000 документах
#        accuracy                           0.80      1200
#       macro avg       0.75      0.68      0.70      1200
#    weighted avg       0.79      0.80      0.79      1200
# Accuracy: 0.7958333333333333

#  для LogisticRegression на всіх данних
#        accuracy                           0.56     18718
#       macro avg       0.54      0.38      0.43     18718
#    weighted avg       0.55      0.56      0.54     18718

# Accuracy: 0.5626135270862271

#%%
'''
одна фіча - нормована сума всіх векторів слів документу, на звичайній нейронній мережі
'''
x_train = np.array(x_train)
x_test = np.array(x_test)
y_train = np.array(y_train)
y_test = np.array(y_test)
model = keras.Sequential([
    # keras.layers.Flatten(input_shape=(len(labels), 300)),
    # keras.layers.Dropout(0.5),
    keras.layers.Dense(900, activation=tf.nn.relu),
    keras.layers.Dropout(0.5),
    # keras.layers.Dense(100, activation=tf.nn.relu),
    keras.layers.Dense(len(labels)+1, activation=tf.nn.softmax)
])
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=3)

test_loss, test_acc = model.evaluate(x_test, y_test)
test_predictions = model.predict(x_test)
predicted_classes = np.argmax(test_predictions, axis=1)
target_names = [k[:15] for k in final_labels]
# print("Accuracy:", accuracy_score(y_test, predicted_classes))
print(classification_report(y_test,  predicted_classes, target_names=target_names))
print('Test accuracy:', test_acc)
#        accuracy                           0.56     18718
#       macro avg       0.52      0.36      0.38     18718
#    weighted avg       0.55      0.56      0.52     18718

# Test accuracy: 0.5556149
#%%
'''
одна фіча - нормована сума всіх векторів слів документу, на звичайній мережі з LSTM та dense шаром
'''
x_train_ = x_train.reshape(len(x_train),300,1)
x_test_ = x_test.reshape(len(x_test),300,1)

model = keras.Sequential([
    # keras.layers.Input(shape=x_train[0].shape),
    # keras.layers.Dense(900, activation=tf.nn.relu),
    # keras.layers.Dense(input_shape=x_train[0].shape, units=300),
    # keras.layers.Embedding(238820, 300),
    # keras.layers.Flatten(input_shape=(len(labels), 300)),
    # keras.layers.Dropout(0.5),
    # keras.layers.Dense(300, activation=tf.nn.relu),
    # keras.layers.Dense(900, activation=tf.nn.relu),
    # keras.layers.LSTM(300)),
    # keras.layers.Reshape((2, 300), input_shape=x_train[0].shape),
    # keras.layers.LSTM(300),
    tf.keras.layers.Bidirectional(keras.layers.LSTM(300)),
    keras.layers.Dropout(0.1),
    # tf.keras.layers.Dense(600, activation='relu'),
    # keras.layers.Flatten(input_shape=(len(labels), 300)),
    
    # keras.layers.Dense(900, activation=tf.nn.relu),
    # keras.layers.Dropout(0.5),
    # keras.layers.Dense(100, activation=tf.nn.relu),
    keras.layers.Dense(len(labels)+1, activation=tf.nn.softmax)
])
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train_, y_train, epochs=1)

test_loss, test_acc = model.evaluate(x_test_, y_test)
test_predictions = model.predict(x_test_)
predicted_classes = np.argmax(test_predictions, axis=1)
target_names = [k[:15] for k in final_labels]
# print("Accuracy:", accuracy_score(y_test, predicted_classes))
print(classification_report(y_test,  predicted_classes, target_names=target_names))
print('Test accuracy:', test_acc)
# Пробував різні варіанти, точність не вище 0.30

#%%
'''
додаємо фічі на основі tfidf
'''
# будуємо на навчальних даних генералізовані документи
# (всі документи однієї категорії об'єднуються в один текст). 
generalized_documents={}
for d in x_train_raw:
    text = ' '.join(d[1])
    category = d[2]
    if category in generalized_documents.keys():
                    generalized_documents[category] = generalized_documents[category] + ' ' + text
    else:
        generalized_documents[category] = ''


# важливий параметр зглажування  sublinear_tf=True - 
# інакше найбільш важливі слова не дуже реалістичні
vectorizer = TfidfVectorizer(sublinear_tf=True)

labels_ = []
corpus = []
for key, value in generalized_documents.items():
    labels_.append(key)
    corpus.append(value)
tfidf_matrix = vectorizer.fit_transform(corpus)
feature_names = vectorizer.get_feature_names()
dense = tfidf_matrix.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names, index=labels_)
s = pd.Series(df.loc[labels_[0]])
# приклад найважливіших слів для катеогрії
s[s > 0].sort_values(ascending=False)[:10]
df_ = df.T
#%%
'''
тільки одна фіча - сумма всіх tfidf ваг слів документу для кожної категорії окремо
'''
start = time.time()
j=0
x_train=[]
for d in x_train_raw:
    #для кадого документа фвормируем вектор, в окторо
    distances_feature=np.zeros(len(labels))
    # distances_feature_vector = np.zeros((len(labels), 300))
    j=j+1
    if j%100==0:
        print(j)
    for w in d[1]:
        # print(w)
        if w in df_.index:
            i=-1
            for label in labels:
                i=i+1
                distances_feature[i] = distances_feature[i] + df_[label][w]
                # distances_feature_vector[i] = distances_feature_vector[i] + df_[label][w] * vector_model.get_vector(w) 
 
    # x_train.append(np.concatenate([d[0], distances_feature]))
    x_train.append(distances_feature/(i+2))
    # x_train.append(distances_feature)
    # x_train.append(d[0])
    # data_res2.append((d[0],d[1],d[2],))
j=0
x_test=[]
for d in x_test_raw:
    #для кадого документа фвормируем вектор, в окторо
    distances_feature = np.zeros(len(labels))
    # distances_feature_vector = np.zeros((len(labels), 300))
    j=j+1
    if j%100==0:
        print(j)
    for w in d[1]:
        if w in df_.index:
            i=-1
            for label in labels:
                i=i+1
                distances_feature[i] = distances_feature[i] + df_[label][w]
                # distances_feature_vector[i] = distances_feature_vector[i] + df_[label][w]*vector_model.get_vector(w)
                
    # x_test.append(np.concatenate([d[0], distances_feature]))
    x_test.append(distances_feature/(i+2))
    # x_test.append(distances_feature)
    # x_test.append(d[0])
    # data_res2.append((d[0],d[1],d[2],))
end = time.time()
print(' _ time elapsed ', end - start)

#%%
x_train = np.array(x_train)
x_test = np.array(x_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

model = keras.Sequential([
    keras.layers.Dense(900, activation=tf.nn.relu),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(len(labels)+1, activation=tf.nn.softmax)
])
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10)

test_loss, test_acc = model.evaluate(x_test, y_test)
test_predictions = model.predict(x_test)
predicted_classes = np.argmax(test_predictions, axis=1)
target_names = [k[:15] for k in final_labels]
# print("Accuracy:", accuracy_score(y_test, predicted_classes))
print(classification_report(y_test,  predicted_classes, target_names=target_names))
print('Test accuracy:', test_acc)

# на 4000 документів
#        accuracy                           0.60      1200
#       macro avg       0.53      0.32      0.34      1200
#    weighted avg       0.64      0.60      0.52      1200

# Test accuracy: 0.5975

#  на 8000 документів
#        accuracy                           0.48      2400
#       macro avg       0.39      0.24      0.24      2400
#    weighted avg       0.49      0.48      0.41      2400
# Test accuracy: 0.485



#%%
'''
фіча - сумма всіх векторів слів зваженими tfidf вагами
'''
start = time.time()
j=0
x_train=[]
for d in x_train_raw:
    #для кадого документа фвормируем вектор, в окторо
    distances_feature=np.zeros(len(labels))
    distances_feature_vector = np.zeros((len(labels), 300))
    j=j+1
    if j%100==0:
        print(j)
    for w in d[1]:
        # print(w)
        if w in df_.index:
            i=-1
            for label in labels:
                i=i+1
                # distances_feature[i] = distances_feature[i] + df_[label][w]
                distances_feature_vector[i] = distances_feature_vector[i] + df_[label][w] * vector_model.get_vector(w) 
 
    # x_train.append(np.concatenate([d[0], distances_feature]))
    x_train.append(distances_feature_vector/(i+2))
    # x_train.append(distances_feature)
    # x_train.append(d[0])
    # data_res2.append((d[0],d[1],d[2],))
j=0
x_test=[]
for d in x_test_raw:
    #для кадого документа фвормируем вектор, в окторо
    distances_feature = np.zeros(len(labels))
    distances_feature_vector = np.zeros((len(labels), 300))
    j=j+1
    if j%100==0:
        print(j)
    for w in d[1]:
        if w in df_.index:
            i=-1
            for label in labels:
                i=i+1
                # distances_feature[i] = distances_feature[i] + df_[label][w]
                distances_feature_vector[i] = distances_feature_vector[i] + df_[label][w]*vector_model.get_vector(w)
                
    # x_test.append(np.concatenate([d[0], distances_feature]))
    x_test.append(distances_feature_vector/(i+2))
    # x_test.append(distances_feature)
    # x_test.append(d[0])
    # data_res2.append((d[0],d[1],d[2],))
end = time.time()
print(' _ time elapsed ', end - start)

#%%
# clf = KNeighborsClassifier(n_neighbors=3)
clf = LogisticRegression()
clf.fit(x_train, y_train) 
predictions = clf.predict(x_test)

print(classification_report(y_test, predictions))
print("Accuracy:", accuracy_score(y_test, predictions))

#%%
x_train = np.array(x_train)
x_test = np.array(x_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(len(labels), 300)),
    # keras.layers.Dropout(0.5),
    # keras.layers.Embedding(238820, 300, input_length=x_train.shape[0])
    keras.layers.Dense(900, activation=tf.nn.relu),
    keras.layers.Dropout(0.5),
    # keras.layers.Dense(900, activation=tf.nn.relu),
    #keras.layers.Dense(315, activation=tf.nn.relu),
    # keras.layers.Dense(100, activation=tf.nn.relu),C
    #keras.layers.Dense(600, activation=tf.nn.relu),
    # keras.layers.Dens
    keras.layers.Dense(len(labels)+1, activation=tf.nn.softmax)
])
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10)

test_loss, test_acc = model.evaluate(x_test, y_test)
test_predictions = model.predict(x_test)
predicted_classes = np.argmax(test_predictions, axis=1)
target_names = [k[:15] for k in final_labels]
# print("Accuracy:", accuracy_score(y_test, predicted_classes))
print(classification_report(y_test,  predicted_classes, target_names=target_names))
print('Test accuracy:', test_acc)

# на 4000 тисяч 
#        accuracy                           0.84      1200
#       macro avg       0.85      0.74      0.78      1200
#    weighted avg       0.84      0.84      0.83      1200

# Test accuracy: 0.84

# на 10 тис документах

# Epoch 10/10
# 6998/6998 [==============================] - 24s 3ms/sample - loss: 0.2710 - acc: 0.9231
# 3000/3000 [==============================] - 3s 857us/sample - loss: 0.5613 - acc: 0.8443
#                  precision    recall  f1-score   support

# Технічне-обслуг       0.70      0.56      0.62       140
# Удосконалення-о       0.71      0.64      0.67        64
# Встановлення-си       0.66      0.81      0.73        84
# Стан-зливосточн       0.50      0.12      0.19        17
# Видалення-аварі       0.98      0.90      0.94        97
# Вилов-безпритул       1.00      0.97      0.99        38
# Паркування-на-з       1.00      0.29      0.45        17
# Незадовільне-ро       0.90      0.87      0.88        61
# Ремонт-під-їзду       0.83      0.89      0.86       365
# Укладання-та-ре       0.97      0.69      0.81        55
# Проведення-дера       0.91      0.66      0.77        62
# Робота-світлофо       0.94      0.93      0.93       145
# Ремонт-та-замін       0.81      0.79      0.80        53
# Ремонт-та-обслу       0.83      0.50      0.62        20
# Про-розгляд-зве       0.61      0.80      0.69       305
# Ремонт-і-обслуг       0.80      0.63      0.70        83
# Незручності-від       0.92      0.67      0.77        18
# Встановлення-па       0.87      0.63      0.73        41
# Незадовільна-ос       1.00      1.00      1.00        17
# Правила-торгове       0.94      0.64      0.76        25
# Незадовільна-те       0.88      0.87      0.87       192
# Незадовільне-об       0.93      0.90      0.91        41
# Відсутність-ГВП       0.94      0.97      0.95       889
# Голів-ОСББ--ЖБК       0.88      0.32      0.47        22
# Відсутність-кан       0.74      0.88      0.80        42
# Нанесення-дорож       0.91      0.92      0.91       107

#        accuracy                           0.84      3000
#       macro avg       0.85      0.72      0.76      3000
#    weighted avg       0.85      0.84      0.84      3000

# Test accuracy: 0.84433335

# на 20000 тис док
#        accuracy                           0.84      5997
#       macro avg       0.82      0.67      0.72      5997
#    weighted avg       0.84      0.84      0.83      5997
# Test accuracy: 0.83558446
#%%
'''
фічі - просто вектор та сумма всіх векторів слів зваженими tfidf вагами
'''
start = time.time()
j=0
x_train=[]
for d in x_train_raw:
    #для кадого документа фвормируем вектор, в окторо
    distances_feature=np.zeros(len(labels))
    distances_feature_vector = np.zeros((len(labels), 300))
    j=j+1
    if j%100==0:
        print(j)
    for w in d[1]:
        # print(w)
        if w in df_.index:
            i=-1
            for label in labels:
                i=i+1
                distances_feature[i] = distances_feature[i] + df_[label][w]
                distances_feature_vector[i] = distances_feature_vector[i] + df_[label][w] * vector_model.get_vector(w) 
 
    x_train.append(np.concatenate([d[0], distances_feature]))
    # x_train.append(distances_feature_vector/(i+2))
    # x_train.append(distances_feature)
    # x_train.append(d[0])
    # data_res2.append((d[0],d[1],d[2],))
j=0
x_test=[]
for d in x_test_raw:
    #для кадого документа фвормируем вектор, в окторо
    distances_feature = np.zeros(len(labels))
    distances_feature_vector = np.zeros((len(labels), 300))
    j=j+1
    # print(j)
    for w in d[1]:
        if w in df_.index:
            i=-1
            for label in labels:
                i=i+1
                distances_feature[i] = distances_feature[i] + df_[label][w]
                distances_feature_vector[i] = distances_feature_vector[i] + df_[label][w]*vector_model.get_vector(w)
                
    x_test.append(np.concatenate([d[0], distances_feature]))
    # x_test.append(distances_feature_vector/(i+2))
    # x_test.append(distances_feature)
    # x_test.append(d[0])
    # data_res2.append((d[0],d[1],d[2],))
end = time.time()
print(' _ time elapsed ', end - start)

#%%
# clf = KNeighborsClassifier(n_neighbors=3)
clf = LogisticRegression()
clf.fit(x_train, y_train) 
predictions = clf.predict(x_test)

print(classification_report(y_test, predictions))
print("Accuracy:", accuracy_score(y_test, predictions))
#     accuracy                           0.81      1200
#    macro avg       0.85      0.69      0.74      1200
# weighted avg       0.82      0.81      0.81      1200

# Accuracy: 0.8133333333333334
#%%
x_train = np.array(x_train)
x_test = np.array(x_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

model = keras.Sequential([
    # keras.layers.Flatten(input_shape=(len(labels), 300)),
    keras.layers.Dense(900, activation=tf.nn.relu),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(len(labels)+1, activation=tf.nn.softmax)
])
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)

test_loss, test_acc = model.evaluate(x_test, y_test)
test_predictions = model.predict(x_test)
predicted_classes = np.argmax(test_predictions, axis=1)
target_names = [k[:15] for k in final_labels]
# print("Accuracy:", accuracy_score(y_test, predicted_classes))
print(classification_report(y_test,  predicted_classes, target_names=target_names))
print('Test accuracy:', test_acc)

# на 4000 тисяч 
#        accuracy                           0.82      1200
#       macro avg       0.80      0.71      0.74      1200
#    weighted avg       0.82      0.82      0.81      1200

# Test accuracy: 0.81666666
# %%
# saving data to pickle
with open('x_train_with_features.pickle', 'wb') as f:
     pickle.dump(x_train, f)
# loadind data
# with open('x_train_with_features.pickle', 'rb') as f:
#      x_train = pickle.load(f)
with open('x_test_with_features.pickle', 'wb') as f:
     pickle.dump(x_test, f)
# loadind data
# with open('x_test_with_features.pickle', 'rb') as f:
#      x_test = pickle.load(f)


