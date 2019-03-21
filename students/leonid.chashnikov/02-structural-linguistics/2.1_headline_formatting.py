import spacy
from spacy.tokens.token import Token

nlp = spacy.load('en_core_web_lg')

input_file = '../../../tasks/02-structural-linguistics/examiner-headlines.txt'
output_file = './2.1-correct_headlines.txt'

big_letter_tag = ['NN', 'PRP', 'VB', 'JJ', 'RB']
Token.set_extension('need_capitalize', default=False)


def _check_token_needs_capitalizing(token):
    pos_big_letter = any(token.tag_.startswith(tag) for tag in big_letter_tag)
    # розрізняти prepositions та subordinate conjunctions
    pos_conjunction = token.pos_ == 'ADP' and len(list(token.children)) == 0
    # hyphen is handled separately
    return pos_big_letter or pos_conjunction


def mark_doc(line: str):
    doc = nlp(line)

    # first word capitalization
    doc[0]._.set('need_capitalize', True)

    for token in doc[1:-1]:
        if token.text != '-':
            needs_capitalization = _check_token_needs_capitalizing(token)
            if needs_capitalization:
                token._.set('need_capitalize', True)
        else:
            doc[token.i - 1]._.set('need_capitalize', True)
            doc[token.i + 1]._.set('need_capitalize', True)
        # print(needs_capitalization)

    # last word capitalization
    doc[-1]._.set('need_capitalize', True)

    return doc


def fix_headline(doc):
    fixed_headline = ''
    for token in doc:
        need_capitalize = token._.get('need_capitalize')
        if need_capitalize and token.is_title:
            fixed_headline += token.text_with_ws
            continue
        if not need_capitalize and not token.is_title:
            fixed_headline += token.text_with_ws
            continue
        if need_capitalize and not token.is_title:
            fixed_headline += token.text_with_ws.capitalize()
            continue
        if not need_capitalize and token.is_title:
            fixed_headline += token.text_with_ws.lower()
            continue
    return fixed_headline


def save_new_headline(line: str, output):
    output.write(line + '\n')


with open(input_file) as inp:
    with open(output_file, mode='w') as out:
        lines = [line.rstrip('\n') for line in inp]
        headlines_changed = 0
        doc_count = 0
        for l in lines:
            doc_count += 1
            doc = mark_doc(l)
            fixed_headline = fix_headline(doc)
            save_new_headline(fixed_headline, out)
            if fixed_headline != l:
                headlines_changed += 1

        print('Document count {}'.format(doc_count))
        print('Fixed formatting for {}'.format(headlines_changed))

