from typing import Dict, Set, List

from .DocumentForEval import DocumentForEval
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

_wordnet_lemmatizer = WordNetLemmatizer()
_english_stopwords = set(stopwords.words('english'))


def retrive_lemmatized_tokens(lang: str, keywords: List[str]) -> Set[str]:
    if lang.lower() != 'en':
        raise ValueError("Only English language is supported at the moment.")
    res = set()
    for kw in keywords:
        for word in word_tokenize(kw):
            lemma = _wordnet_lemmatizer.lemmatize(word.casefold())
            if lemma in _english_stopwords:
                continue
            res.add(lemma)
    return res


def evaluate_keywords(document: DocumentForEval) -> Dict[str, float]:
    ref_tokens: Set[str] = retrive_lemmatized_tokens(document.lang, document.ref_keywords)
    tokens: Set[str] = retrive_lemmatized_tokens(document.lang, document.keywords)
