import pickle
import langdetect


def _read_comments():
    result = []
    with open('./comments.p', 'rb') as f:
        while 1:
            try:
                result.append(pickle.load(f))
            except EOFError:
                break  # no more data in the file
    flat_result = [item for sublist in result for item in sublist]
    return flat_result


def _filter_out_by_lang(comments):
    results = []
    for comment in comments:
        try:
            lang = langdetect.detect(comment['text'])
            if lang == 'uk':
                results.append(comment)
        except Exception as e:
            print(e)
    return results


def _classify(ukr_comments):
    result = []
    for comment in ukr_comments:
        if comment.get('rating') in ('4', '5'):
            result.append(dict(label='pos', text=comment['text']))
        if comment.get('rating') == '3':
            result.append(dict(label='neu', text=comment['text']))
        if comment.get('rating') in ('1', '2'):
            result.append(dict(label='neg', text=comment['text']))
    return result


def _save_comments(classified_comments):
    with open('processed_comments.p', 'wb') as fp:
        pickle.dump(classified_comments, fp)


if __name__ == "__main__":
    comments = _read_comments()
    print(len(comments))
    ukr_comments = _filter_out_by_lang(comments[0:100])
    print(len(ukr_comments))
    classified_comments = _classify(ukr_comments)
    print(len(classified_comments))
    _save_comments(classified_comments)
