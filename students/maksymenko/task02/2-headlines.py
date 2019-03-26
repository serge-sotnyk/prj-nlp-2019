import en_core_web_md
nlp = en_core_web_md.load()

PROPN = 'PROPN'
NOUN = 'NOUN'
PRON = 'PRON'
VERB = 'VERB'
ADJ = 'ADJ'
ADV = 'ADV'
ADP = 'ADP'

INPUT_FILE = 'tasks/02-structural-linguistics/examiner-headlines.txt'
OUTPUT_FILE = 'students/maksymenko/task02/formatted-headlines.txt'

capitalizable_pos = [PROPN, NOUN, PRON, VERB, ADJ, ADV]


def capitalize(token):
    return token.text_with_ws.capitalize()


def to_lowercase(token):
    return token.text_with_ws.lower()


def format_headline(string):
    formatted_headline = []

    for idx, token in enumerate(string):
        if idx == 0:
            formatted_headline.append(capitalize(token))
            continue

        if token.pos_ == VERB and token.text.startswith("'"):
            formatted_headline.append(token.text_with_ws)
            continue

        if idx == len(string) - 1:
            formatted_headline.append(capitalize(token))
            continue

        if token.pos_ == PROPN and token.is_upper:
            formatted_headline.append(token.text_with_ws)
            continue

        if token.pos_ == ADP and len(list(token.children)) == 0:
            formatted_headline.append(capitalize(token))
            continue

        if token.pos_ in capitalizable_pos:
            formatted_headline.append(capitalize(token))
        else:
            formatted_headline.append(to_lowercase(token))

    return "".join(formatted_headline)


def format_headlines(input_file_path, output_file_path, lines_num, debug=False):
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        with open(output_file_path, 'w+', encoding='utf-8') as output_file:
            formatted_count = 0

            for idx, line in enumerate(input_file):
                if idx <= lines_num - 1:
                    headline = nlp(line)
                    formatted_headline = format_headline(headline)

                    if not debug:
                        output_file.write(formatted_headline)

                    if line != formatted_headline:
                        formatted_count += 1
                        if debug:
                            print(f'Line {idx}: {line}')
                            print(f'Line {idx}: {formatted_headline}')
            print(f'Formatted {formatted_count} lines from total {lines_num}')


# format_headlines(INPUT_FILE, OUTPUT_FILE, 5, True)
format_headlines(INPUT_FILE, OUTPUT_FILE, 5000)

# Formatted 4432 lines from total 5000