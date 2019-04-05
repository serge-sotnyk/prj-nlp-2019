from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

from .EmbVectorizer import EmbVectorizer
from .StatVectorizer import StatVectorizer
from .ToneVectorizer import ToneVectorizer
from .uk_utils import tokenize_lemmatize


def create_pipeline() -> Pipeline:
    def tokenizer(text: str):
        return tokenize_lemmatize(text)

    features = FeatureUnion([
            ('bow_features', Pipeline([
                ('bow', TfidfVectorizer(tokenizer=tokenizer)),
                ('scaler', StandardScaler(with_mean=False))
            ])),
            ('stat_features', Pipeline([
                ('text_stat', StatVectorizer()),
                ('scaler', StandardScaler())
            ])),
            ('emb_features', Pipeline([
                ('embs', EmbVectorizer()),
                ('scaler', StandardScaler())
            ])),
            ('tone_features', Pipeline([
                ('text_tone', ToneVectorizer()),
                ('scaler', StandardScaler()),
            ]))
        ],
        transformer_weights={
            'bow_features': 1,
            'stat_features': 0.02,
            'emb_features': 0.5,
            'tone_features': 0.02,
        }
    )

    steps = [
        ('feat_union', features),
        # ('vectorize', TfidfVectorizer(tokenizer=tokenizer)),
        # ('reductor', TruncatedSVD(n_components=100)),
        ('classifier', SGDClassifier(max_iter=1000, tol=1e-3))
        # ('classifier', RandomForestClassifier())
    ]

    return Pipeline(steps)
