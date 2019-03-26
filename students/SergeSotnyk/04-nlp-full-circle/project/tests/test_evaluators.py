from os import path

from keysum_evaluator import *

__location__ = path.dirname(__file__)


def test_retrive_lemmatized_tokens():
    keywords = ['Technics', 'to be or not to be', 'Kings']
    lemmatized_tokens = retrive_lemmatized_tokens('en', keywords)
    assert len(lemmatized_tokens) == 2
    assert 'king' in lemmatized_tokens
