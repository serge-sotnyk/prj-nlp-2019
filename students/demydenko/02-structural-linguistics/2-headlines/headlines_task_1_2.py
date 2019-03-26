import re
import spacy
import en_core_web_lg
from spacy.tokenizer import Tokenizer
from spacy.util import compile_prefix_regex, compile_suffix_regex

from sentiment_power_test import sentiment_power


def custom_tokenizer(nlp):
    # infix_re = re.compile(r'''[.\,\?\:\;\...\‘\’\“\”\"]''')
    infix_re = re.compile(r'''[.\,\?\:\;\...\‘\’\`\“\”\"\'~]''')
    prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)

    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                     suffix_search=suffix_re.search,
                     infix_finditer=infix_re.finditer,
                     token_match=None)


def print_original_heading_and_new_tokens_list(doc, new_tokens_list):
    [print("{:<15}{:<15}{:<7}{:<7}{:<15}".
           format(token.text, str(new_tokens_list[i]),  token.pos_, token.tag_, spacy.explain(token.pos_)))
     for i, token in enumerate(doc)]


def proceed_headline(original_string, print_result=False):
    doc_contains_comp_super = False
    doc_contains_NE = False

    doc = nlp(original_string)
    new_list = [token.text for token in doc]

    # always change first and last token
    for k, token in enumerate(doc):
        if token.text[0].isalpha():
            new_list[k] = new_list[k].title()
            break

    for i, token in reversed(list(enumerate(doc))):
        if token.text[0].isalpha():
            new_list[k] = new_list[k].title()
            break

    # was wrong!
    # new_list[0] = new_list[0].title()
    # new_list[-1] = new_list[-1].title()

    # POS test
    for ind, token in enumerate(doc):
        if token.pos_ in ['VERB', 'NOUN',  'PRON', 'ADJ', 'ADV', 'SCONJ']:
            # exception
            exceptions = ["'s", "ll", 't']
            if token.text not in exceptions:
                new_list[ind] = new_list[ind].title()
        if token.pos_ == 'ADP' and token.dep_ == 'mark':
            new_list[ind] = new_list[ind].title()

        if token.tag_ in ['JJS', 'JJR', 'RBS', 'RBR']:
            doc_contains_comp_super = True

    # new heading construction
    result_string = ''
    for ind, token in enumerate(doc):
        result_string = result_string + new_list[ind] + str(token.whitespace_)

    # NER test
    result_ents_labels = list()
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'NORP', 'MONEY', 'GPE', 'ORG']:
            result_ents_labels.append(ent.label_)
            doc_contains_NE = True

    # sentiment power test
    sentiment_power_ = sentiment_power(original_string)

    if print_result:
        print("original string  = ", original_string)
        print("result string    = ", result_string)
        print_original_heading_and_new_tokens_list(doc, new_list)
        print("ents_labels  = ", result_ents_labels)
        print("sentiment_power_  = ", sentiment_power_)

    return result_string, doc_contains_comp_super, doc_contains_NE, sentiment_power_


print('loading model...')
nlp = en_core_web_lg.load()
# nlp = en_core_web_md.load()
nlp.tokenizer = custom_tokenizer(nlp)

# # tests
# test1 = proceed_headline("It's a nice trip. Don't Miss Bridal Event! I'll be.", print_result=True)
# test2 = proceed_headline("'psych' season premiere date revealed as eBay: 'the musical'", print_result=True)
# test3 = proceed_headline("Do as you want", print_result=True)
# test3 = proceed_headline("How to use a Macbook as a table", print_result=True)


print('loading data...')
with open('data/examiner-headlines.txt') as f:
    headlines = f.readlines()
headlines = [x.strip() for x in headlines]
headlines_result = list()
headlines_sentiment_power = list()

print('parsing...')
count_of_unchanged = 0
count_of_headings_with_ents = 0
count_of_headings_with_comp_super = 0

i = 0
for headline in headlines:
    res = proceed_headline(headlines[i])
    headline_after_proceeding = res[0]
    doc_contains_comp_super = res[1]
    doc_contains_NE = res[2]
    sentiment_power_ = res[3]
    viral_coef_comp_super = 0
    viral_coef_ner = 0

    # unchanged stat
    if headline == headline_after_proceeding:
        count_of_unchanged += 1

    # comp_super stat
    if res[1]:
        count_of_headings_with_comp_super += 1

    # NER stat
    if res[2]:
        count_of_headings_with_ents += 1

    k1 = 0
    if doc_contains_comp_super:
        k1 = 0.1
    k2 = 0
    if doc_contains_NE:
        k2 = 0.1

    viral_coef = k1 + k2 + sentiment_power_[0]

    headlines_sentiment_power.append((headline_after_proceeding, viral_coef, sentiment_power_))

    headlines_result.append(headline_after_proceeding)
    i += 1
    if i % 100 == 0:
        print('headlines parsed-', i)

# saving results
with open('data/examiner-headlines-result.txt', 'w') as f:
    for item in headlines_result:
        f.write("%s\n" % item)
print('results:')
print('кількість заголовків залишились незмінними - ', count_of_unchanged)
print('кількість заголовків із ступенями порівяння - ', count_of_headings_with_comp_super)
print("кількість заголовків із сутностями типу 'PERSON', 'NORP', 'MONEY', 'GPE', 'ORG'  - ",
      count_of_headings_with_ents)
top10viral = sorted(headlines_sentiment_power, key=lambda x: x[1], reverse=True)
print('top 10 viral headings')
[print(h) for h in top10viral[0:9]]