import spacy

nlp = spacy.load('en_core_web_lg', disable=['ner'])
headlines = []
capitalize = { 
    'NN', 'NNP', 'NNPS', 'NNS', 'PRP', 'PRP$', 'WP', 'WP$', 
    'JJ', 'JJR', 'JJS', 'BES', 'HVS', 'MD', 'VB', 'VBD', 'VBG',
    'VBN', 'VBP', 'VBZ', 'RB', 'RBR', 'RBS', 'RP', 'WRB', 'IN'
}

with open('../../../../tasks/02-structural-linguistics/examiner-headlines.txt') as f:
    for line in f:
        headline = []
        follower = False
        paired_opened = False
        doc = nlp(line.strip())

        for token in doc:
            text, pos, tag, dep = token.text, token.pos_, token.tag_, token.dep_
            if text[0] == "'" and pos != 'PUNCT':
                headline[-1] += text
            elif token.is_punct and tag != 'LS':
                if len(doc) - 1 == token.i:
                    headline[-1] += text
                elif text == '--':
                    headline[-1] += '—'
                    follower = True
                    continue
                elif tag == "``" or tag == "''":
                    if paired_opened:
                        headline[-1] += text
                        paired_opened = False
                    else:
                        headline.append(text)
                        follower = True
                        paired_opened = True
                        continue
                elif tag == 'HYPH' or text == '-':
                    headline[-1] += text
                    follower = True
                    continue
                elif token.is_left_punct:
                    headline.append(text)
                    follower = True
                    continue
                else:
                    headline[-1] += text
            elif pos == 'SYM': 
                if dep == 'quantmod' or dep == 'nmod':
                    headline.append(text)
                    follower = True
                else:
                    headline[-1] += text
                    follower = True
                continue
            elif text == '%':
                headline[-1] += text
            elif text == text.upper():
                headline.append(text)
            elif tag in capitalize and dep != 'prep':
                headline.append(text.capitalize())
            else:
                headline.append(text.lower())
            if follower:
                t = headline[-1]
                headline[-2] += headline[-1]
                headline.pop()
                follower = False
        
        leading_word, trailing_word = headline[0], headline[-1]
        leading_wordList, trailing_wordList = list(leading_word), list(headline[-1])

        if leading_word != leading_word.upper():
            if leading_wordList[0].isalpha():
                headline[0] = leading_word.capitalize()
            else:
                leading_wordList[1] = leading_wordList[1].upper()
                headline[0] = ''.join(leading_wordList)
        if trailing_word != trailing_word.upper():
            if trailing_word[0].isalpha():
                headline[-1] = trailing_word.capitalize()
            else:
                trailing_wordList[1] = trailing_wordList[1].upper()
                headline[-1] = ''.join(trailing_wordList)

        headlines.append(headline)


with open('1-formatting.txt', 'r+') as output:
    output.truncate(0)
    output.write('\n'.join([' '.join(x) for x in headlines]))
