# продовжте синонімний ряд дієслів: "say", "tell", "speak", "claim", "communicate"
# напишіть функцію, яка знаходить у реченні дієслово (за складеним раніше синонімним рядом) і витягає усі можливі прислівники на "-ly", якими це дієслово керує
# напишіть програму, яка знайде усі можливі прислівники для наших дієслів у корпусі блогів
# на виході програма повинна видати десять найчастотніших прислівників для кожного дієслова (разом із частотою). Приклад виводу:

from nltk.corpus import wordnet as wn
import en_core_web_md
import json

nlp = en_core_web_md.load()

initial_verbs = ["say", "tell", "speak", "claim", "communicate"]
INPUT_FILE = 'tasks/02-structural-linguistics/blog2008.txt'


def extend_verbs_with_syns(initial_verbs):
    syn_verbs = []

    for verb in initial_verbs:
        synset = wn.synsets(verb, 'v')

        for s in synset:
            syn_verbs.append(s.name().split('.')[0])

    return list(set(initial_verbs + syn_verbs))


def save_collocations(lines_count, collocations):
    data = {'lines_count': lines_count, 'collocations': collocations}
    file = open('students/maksymenko/task02/collocations.txt', 'w+', encoding='utf-8')
    file.write(json.dumps(data))
    file.close()
    print('saved')


def load_collocations():
    file = open('students/maksymenko/task02/collocations.txt', 'r', encoding='utf-8')
    data = json.load(file)
    file.close()

    print(f'Loaded collocations for previously processed {data["lines_count"]} lines')

    return data


def get_initial_collocations(verbs):
    collocations = {}

    for verb in verbs:
        collocations[verb] = {}


def get_collocations(verbs):
    saved_data = load_collocations()
    saved_lines_count = saved_data['lines_count']
    saved_collocations = saved_data['collocations']

    print(saved_lines_count)
    print(saved_collocations)

    collocations = saved_collocations or get_initial_collocations(verbs)

    with open(INPUT_FILE, 'r', encoding='utf-8') as input_file:
        lines_count = saved_lines_count or 0

        for idx, line in enumerate(input_file):
            if idx < lines_count:
                continue

            lines_count += 1

            if idx % 100 == 0:
                print(idx)

            if idx % 10000 == 0 and idx != saved_lines_count:
                save_collocations(idx, collocations)


            nlp_line = nlp(line)
            for token in nlp_line:
                if token.pos_ == 'VERB' and token.lemma_ in verbs:
                    subtree = token.subtree
                    for mod in subtree:
                        # print(child.text)
                        if mod.pos_ == 'ADV' and mod.text.endswith('ly'):
                            try:
                                collocations[token.lemma_][mod.text.lowercase()] += 1
                            except:
                                collocations[token.lemma_][mod.text.lowercase()] = 1
                            # print(f'verb {token.text} - child {child.text}')

    save_collocations(lines_count, collocations)

    return collocations

verbs = extend_verbs_with_syns(initial_verbs)
collocations = get_collocations(verbs)

print('done')

def format(collocations):
    formatted = ''

    for verb in sorted(collocations.keys()):
        top10_adverbs = sorted(list(collocations[verb].items()), key=lambda adverb_tuple: adverb_tuple[1], reverse=True)[:10]
        formatted += f'{verb}: '

        for idx, adverb_tuple in enumerate(top10_adverbs):
            eol_sym = ', ' if idx < len(top10_adverbs) - 1 else ''
            formatted += f'{adverb_tuple}{eol_sym}'

        formatted += '\n'

    return formatted

formatted = format(collocations)

print(formatted)

file = open('students/maksymenko/task02/collocations-formatted.txt', 'w')
file.write(formatted)
file.close()
