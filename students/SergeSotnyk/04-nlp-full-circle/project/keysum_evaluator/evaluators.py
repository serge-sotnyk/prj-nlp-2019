from typing import Dict, Set, List

from .DocumentForEval import DocumentForEval
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sumeval.metrics.rouge import RougeCalculator
from sumeval.metrics.bleu import BLEUCalculator

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
    tp = len(ref_tokens.intersection(tokens))
    fp = len(tokens)-tp
    fn = len(ref_tokens)-tp
    eps = 1e-6
    precision = tp / (tp+fp+eps)
    recall = tp / (tp+fn+eps)
    f1 = 2*(precision*recall)/(precision+recall+eps)
    res = {'precision': precision,
           'recall': recall,
           'f1': f1}
    return res


rouge_en = RougeCalculator(stopwords=True, lang="en")
bleu = BLEUCalculator()


def evaluate_summary(document: DocumentForEval) -> Dict[str, float]:
    summary = '\n'.join(document.summary)
    ref_summary = '\n'.join(document.ref_summary)
    if document.lang.lower()!='en':
        raise ValueError("Only English language is supported at the moment.")

    rouge_1 = rouge_en.rouge_n(
        summary=summary,
        references=ref_summary,
        n=1)

    rouge_2 = rouge_en.rouge_n(
        summary=summary,
        references=ref_summary,
        n=2)

    rouge_3 = rouge_en.rouge_n(
        summary=summary,
        references=ref_summary,
        n=3)

    rouge_4 = rouge_en.rouge_n(
        summary=summary,
        references=ref_summary,
        n=4)

    bleu_score = bleu.bleu(
        summary=summary,
        references=ref_summary)

    res = {'rouge_1': rouge_1,
           'rouge_2': rouge_2,
           'rouge_3': rouge_3,
           'rouge_4': rouge_4,
           'bleu': bleu_score}
    return res
