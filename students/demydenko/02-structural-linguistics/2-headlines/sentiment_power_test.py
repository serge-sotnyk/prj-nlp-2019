from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import sent_tokenize, word_tokenize, pos_tag


lemmatizer = WordNetLemmatizer()


def __penn_to_wn(tag):
    """
    Convert between the PennTreebank tags to simple Wordnet tags
    """
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None


def sentiment_power(text):

    sentiment_total_p = 0.0
    sentiment_total_n = 0.0
    tokens_count = 0

    raw_sentences = sent_tokenize(text)
    for raw_sentence in raw_sentences:
        tagged_sentence = pos_tag(word_tokenize(raw_sentence))

        for word, tag in tagged_sentence:
            wn_tag = __penn_to_wn(tag)
            if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                continue

            lemma = lemmatizer.lemmatize(word, pos=wn_tag)
            if not lemma:
                continue

            synsets = wn.synsets(lemma, pos=wn_tag)
            if not synsets:
                continue

            sentiment_p = 0
            sentiment_n = 0
            k = 0
            for synset in synsets:
                k += 1
                if k < 5:
                    swn_synset = swn.senti_synset(synset.name())
                    sentiment_p += swn_synset.pos_score()
                    sentiment_n += swn_synset.neg_score()
                else:
                    break


            sentiment_p_avg = 0
            sentiment_n_avg = 0
            # sentiment_p_avg += sentiment_p / len(synsets)
            # sentiment_n_avg += sentiment_n / len(synsets)
            sentiment_p_avg += sentiment_p / k
            sentiment_n_avg += sentiment_n / k

            sentiment_total_p += sentiment_p_avg
            sentiment_total_n += abs(sentiment_n_avg)
            tokens_count += 1
            # synset = synsets[0]
            # swn_synset = swn.senti_synset(synset.name())
            #
            # sentiment += swn_synset.pos_score() - swn_synset.neg_score()
            # tokens_count += 1

    if not tokens_count:
        return (0,0,0)

    sentiment_power_ = (sentiment_total_p + sentiment_total_n) / tokens_count
    #TODO sentiment_power_with_contract_ = (sentiment_total_p + sentiment_total_n) / tokens_count

    return (sentiment_power_, sentiment_total_p / tokens_count, sentiment_total_n /  tokens_count)

# print (swn_polarity('Montreal area classic car events for July 8-14, 2013'))
# Montreal area classic car events for July 8-14, 2013
# Online Parenting Classes Can Help Build A Healthy Co-Parenting Relationship'
# Movie Star Rip Torn arrested for drunken bank robbery attempt.
# No Justice No Peace