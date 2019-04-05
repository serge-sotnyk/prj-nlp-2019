from sklearn.metrics import f1_score
from tone import create_pipeline, stars_to_sentiment
import pandas as pd
import numpy as np


def main():
    # load data
    df_learn = pd.read_csv('rozetka_learn.csv')
    df_test = pd.read_csv('rozetka_test.csv')
    X_learn = df_learn['review'].values
    X_test = df_test['review'].values
    y_learn = stars_to_sentiment(df_learn['stars'].values)
    y_test = stars_to_sentiment(df_test['stars'].values)

    # learn
    model = create_pipeline()
    model.fit(X_learn, y_learn)

    # estimate
    y_pred = model.predict(X_test)
    score = f1_score(y_test, y_pred, average=None)
    print(f"F1 score = {score}, mean = {np.mean(score)}")


if __name__ == '__main__':
    main()
