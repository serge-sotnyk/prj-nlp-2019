import click
import spacy


def correct_noun(token):
    """
    to avoid "eBay" -> "EBay" or "Ebay"
    """
    return token.pos_ in ('PROPN', 'NOUN') and not token.text.islower()


def short_adv(token):
    """
    to avoid "can't" => "CaN't"
    """
    return token.pos_ == 'ADV' and "'" in token.shape_[1:-1]


def mark_word(token):
    token._.protected = correct_noun(token) or short_adv(token)
    return token


def make_lower(text):
    return text.lower()


def update_by_pos(token, text):
    if token.pos_ in ('NOUN', 'PROPN', 'PRON', 'VERB', 'ADJ', 'ADV'):
        text = text[0].upper() + text[1:]
    return text


def update_sub_conjunction(token, text):
    if token.pos_ == 'ADP' and token.dep_ == 'mark':
        text = text[0].upper() + text[1:]
    return text


def is_word(token):
    return any([i in token.shape_ for i in 'xXd'])


def update_letter(word, letter_ind):
    return word[:letter_ind] + word[letter_ind].upper() + word[letter_ind + 1:]


def get_first_word(doc):
    for token in doc:
        if is_word(token):
            return token


def get_last_word(doc):
    for token in reversed(doc):
        if is_word(token):
            return token


def get_first_symbol(shape):
    allowed_symbols = "Xxd'"
    letter_indexes = [shape.find(i) for i in allowed_symbols]
    letter_indexes = filter(lambda x: x!=-1, letter_indexes)
    return min(letter_indexes, default=None)


def update_edge_word(edge_token, words):
    if not edge_token:
        return words
    
    letter_ind = get_first_symbol(edge_token.shape_)
    if letter_ind is None:
        return words

    words[edge_token.i] = update_letter(words[edge_token.i], letter_ind)
    return words


def update_first_word(doc, words):
    return update_edge_word(get_first_word(doc), words)


def update_last_word(doc, words):
    return update_edge_word(get_last_word(doc), words)


def update_with_hyphen(doc, words):
    for token in doc:
        try:
            if token.nbor().text_with_ws == '-':
                words[token.i] = words[token.i][0].upper() + words[token.i][1:]
                next_token = token.nbor().nbor()
                words[next_token.i] = words[next_token.i][0].upper() + words[next_token.i][1:]
        except IndexError:
            pass
    return words

    
def parse_row(nlp, line):
    doc = nlp(line)
    words = []
    for token in doc:
        token = mark_word(token)
        text = make_lower(token.text_with_ws)
        text = update_by_pos(token, text)
        text = update_sub_conjunction(token, text)
        words.append(text)
    words = update_first_word(doc, words)
    words = update_last_word(doc, words)
    words = update_with_hyphen(doc, words)
    for token in doc:
        if token._.protected:
            words[token.i] = token.text_with_ws
    return ''.join(words)
    

def init():
    print('Loading spacy module', end='')
    nlp = spacy.load('en_core_web_md')
    spacy.tokens.Token.set_extension('protected', default=False)
    print ('.... done')
    return nlp


def run_sentence(sentence):
    nlp = init()
    print(parse_row(nlp, sentence))


def run_file(input, output):
    nlp = init()
    c_updated = 0
    c_total = 0
    try:
        with open(output, 'w') as fout:
            for line in open(input):
                updated = parse_row(nlp, line)
                fout.write(parse_row(nlp, line))
                c_updated += not (updated == line)
                c_total += 1
        print('\nIt was updated', c_updated, 'lines from ', c_total)
    except OSError as e:
        print ('An error has happened:', e)


@click.command()
@click.option('--input', help='Name of income file')
@click.option('--output', default='out.txt', help='Name of outcome file')
@click.argument('sentence', required=False)
def main(input, output, sentence):
    if sentence:
        return run_sentence(sentence)
    if input:
        return run_file(input, output)

    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()


if __name__ == "__main__":
    main()

