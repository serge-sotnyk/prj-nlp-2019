import spacy
from bs4 import BeautifulSoup
from collections import Counter

nlp = spacy.load('en_core_web_md')


def clean_text(raw_text):
    soup = BeautifulSoup(raw_text, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text()


def find_verb_frequency(filename, most_common_number):
    with open(filename, 'r', encoding='ISO-8859-1') as input_file:
        verbs = []
        while True:
            block = input_file.read(1000000)
            if not block:
                break
            block = clean_text(block)
            doc = nlp(block)
            verbs += [token.text.lower() for token in doc if token.pos_ == 'VERB']
    verb_frequency = Counter(verbs)
    most_common_verbs = verb_frequency.most_common(most_common_number)
    with open('common_crawl_output.txt', 'w') as output_file:
        output_file.write('\n'.join('{} {}'.format(x[0], str(x[1])) for x in most_common_verbs))


if __name__ == "__main__":
    find_verb_frequency('CC-MAIN-20160624154951-00043-ip-10-164-35-72.ec2.internal.warc', 100)
