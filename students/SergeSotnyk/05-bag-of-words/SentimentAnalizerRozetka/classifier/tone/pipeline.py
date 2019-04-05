from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

from tone.StatVectorizer import StatVectorizer
from .uk_utils import tokenize_lemmatize


def create_pipeline() -> Pipeline:
    def tokenizer(text: str):
        return tokenize_lemmatize(text)

    features = FeatureUnion([
            ('bow_features', Pipeline([('bow', TfidfVectorizer(tokenizer=tokenizer))])),
            ('stat_features', Pipeline([
                ('text_stat', StatVectorizer()),
                ('scaler', StandardScaler()),
            ]))
        ],
        transformer_weights={
            'bow_features': 1,
            'stat_features': 0.01
        }

    )

    steps = [
        ('feat_union', features),
        # ('vectorize', TfidfVectorizer(tokenizer=tokenizer)),
        # ('reductor', TruncatedSVD(n_components=100)),
        ('classifier', SGDClassifier())
        # ('classifier', RandomForestClassifier())
    ]

    return Pipeline(steps)
