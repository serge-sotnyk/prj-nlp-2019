import langdetect
from langdetect.lang_detect_exception import LangDetectException
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
from urllib.parse import urlparse
# extract individual items,
# perform basic statistical analysis (distribution of
#   hosts,
#   domains )
# and visualization (optional).


def _update_dict(word, counts: dict):
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1


def _get_host(record):
    # or get Host ?
    target_uri = record.rec_headers.get_header('WARC-Target-URI')
    parsed_uri = urlparse(target_uri)
    return parsed_uri.hostname


def _update_word_count(page, counts: dict):
    # stem? filter out symbols
    words = page.text.split()

    for word in words:
        if word not in ['{', '}', '=', '-', '+', '>', '<']:
            _update_dict(word, counts)

    return counts


def _update_language_count(page, counts: dict):
    if page.text:
        try:
            lang = langdetect.detect(page.text)
            _update_dict(lang, counts)
        except LangDetectException as e:
            print(e)


if __name__ == "__main__":
    word_counts = dict()
    lang_counts = dict()
    i = 0
    with open('./data/CC-MAIN-20190116031807-20190116053807-00514.warc', 'rb') as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                i += 1
                content = record.content_stream().read()
                page = BeautifulSoup(content, 'html.parser')

                host = _get_host(record)
                _update_word_count(page, word_counts)
                _update_language_count(page, lang_counts)

                if i % 100 == 0:
                    top_words = sorted(word_counts, key=word_counts.get, reverse=True)[:7]
                    top_langs = sorted(lang_counts, key=lang_counts.get, reverse=True)[:7]
                    print('After processing {} records,\n top words: {}\n top langs: {}\n'
                          .format(i, list(top_words), list(top_langs)))
