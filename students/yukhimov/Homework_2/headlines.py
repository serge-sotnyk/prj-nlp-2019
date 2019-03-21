import re
import spacy
from spacy.tokenizer import Tokenizer

nlp = spacy.load('en_core_web_md')
CAPITALIZED_POS = ('NOUN', 'PROPN', 'PRON', 'VERB', 'ADJ', 'ADV', 'SCONJ')

prefix_re = re.compile(r'^[[(]')
suffix_re = re.compile(r'[])]$')
infix_re = re.compile(r'^$')


def custom_tokenizer(nlp):
    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                infix_finditer=infix_re.finditer)


def capitalize_headlines(headline):
    nlp.tokenizer = custom_tokenizer(nlp)
    doc = nlp(headline)
    tagged_headline = [(token.text, token.pos_) for token in doc]
    normalized_headline = []
    for word, pos in tagged_headline:
        if pos in CAPITALIZED_POS:
            if word.startswith("'"):
                word = "'" + word[1:].capitalize()
            else:
                word = word.capitalize()
        normalized_headline.append(word)
    if normalized_headline[0].startswith("'"):
        normalized_headline[0] = "'" + normalized_headline[0][1:].capitalize()
    else:
        normalized_headline[0] = normalized_headline[0].capitalize()
    normalized_headline[-1] = normalized_headline[-1].capitalize()
    normalized_headline_string = ' '.join(normalized_headline)
    normalized_headline_string = re.sub("(?<=[(\[]) | (?=[)\]])", "", normalized_headline_string)
    return normalized_headline_string


def process_file(filename):
    counter = 0
    changed_headlines = 0
    with open(filename, "r") as input_file:
        with open('processed_headlines.txt', "w") as output_file:
            for line in input_file:
                new_line = capitalize_headlines(line)
                output_file.write(new_line)
                counter += 1
                if new_line.strip() != line.strip():
                    changed_headlines += 1
    with open('headlines_results.txt', "w") as output_file:
        output_file.write('Changed: {}\n'.format(str(changed_headlines)))
        output_file.write('Unchanged: {}'.format(str(counter - changed_headlines)))


if __name__ == "__main__":
    process_file('examiner-headline.txt')
