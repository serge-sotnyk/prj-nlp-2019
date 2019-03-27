import spacy
from collections import Counter

nlp = spacy.load('en_core_web_md')


def find_noun_frequency(filename, most_common_number):
    with open(filename, 'r', encoding='ISO-8859-1') as input_file:
        nouns = []
        while True:
            block = input_file.read(1000000)
            if not block:
                break
            doc = nlp(block)
            nouns += [token.text.lower() for token in doc if token.pos_ == 'NOUN']
    noun_frequency = Counter(nouns)
    most_common_nouns = noun_frequency.most_common(most_common_number)
    with open('common_crawl_output.txt', 'w') as output_file:
        output_file.write('\n'.join('{} {}'.format(x[0], str(x[1])) for x in most_common_nouns))


if __name__ == "__main__":
    find_noun_frequency('CC-MAIN-20160624154951-00043-ip-10-164-35-72.ec2.internal.warc', 100)
