from collections import defaultdict
from itertools import zip_longest
from typing import List, Optional, Dict

import spacy
import wikipedia
import os

_start_tag = '<*'
_finish_tag = '*>'
print('Start downloading spacy')
_nlp = spacy.load("en_core_web_md")
print('Spacy has been downloaded')


class _NotThisSuspect(Exception):
    ...


class Entry:
    def __init__(self, start: int, finish: int):
        self.start = start
        self.finish = finish


class Annotation:
    def __init__(self, text: str = '', entries: List[Entry] = None):
        self.text = text
        self.entries = entries if entries else []


class Checker:
    def __init__(self, tsv_name: str):
        self._lemma_dict = defaultdict(list)
        self._first_lemmas_dict = defaultdict(list)
        for rec in self.load_writings_tsv(tsv_name):
            doc = _nlp(rec)
            lemmas = [w.lemma_.casefold() for w in doc]
            self._first_lemmas_dict[lemmas[0]].append(lemmas)
            for l in lemmas:
                self._lemma_dict[l].append(lemmas)

    def max_len(self):
        mx = 0
        max_lemmas_set = []
        for lemmas_list_set in self._first_lemmas_dict.values():
            for lemmas in lemmas_list_set:
                l = len(lemmas)
                if l > mx:
                    mx = l
                    max_lemmas_set = lemmas
        print(max_lemmas_set)
        # res = max(len(lemmas) for lemmas in [lemmas_list_set for lemmas_list_set in self._first_lemmas_dict])
        return mx

    def _check1(self, suspect_lemmas: List[str]) -> bool:
        for l in suspect_lemmas:  # check if all suspect's lemmas is in the vocabulary
            if l not in self._lemma_dict:
                return False
        for cluster in self._lemma_dict[suspect_lemmas[0]]:  # check a lemmas order and size
            if len(suspect_lemmas) != len(cluster):
                continue
            for a, b in zip_longest(suspect_lemmas, cluster):
                if a != b:
                    continue
            return True
        return False

    def check_with_order(self, suspect_lemmas: List[str]) -> bool:
        if suspect_lemmas[0] not in self._first_lemmas_dict:
            return False
        if lemmas_starts_with(suspect_lemmas, ['call', 'me', 'joe']):
            ...
        for lemmas in self._first_lemmas_dict[suspect_lemmas[0]]:
            try:
                if len(lemmas) != len(suspect_lemmas):
                    raise _NotThisSuspect()
                for a, b in zip(lemmas, suspect_lemmas):
                    if a != b:
                        raise _NotThisSuspect()
                return True
            except _NotThisSuspect:
                continue
        return False

    def check(self, suspect: str) -> bool:
        doc = _nlp(suspect)
        lemmas = [w.lemma_.casefold() for w in doc]
        return self._check1(lemmas)

    @staticmethod
    def load_writings_tsv(tsv_name: str) -> List[str]:
        res = []
        with open(tsv_name, 'rt', encoding='utf-8') as f:
            next(f)  # skip titles
            for line in f:
                name, collection = line.split('\t')
                name = name.strip().replace('"', '')
                name = name.split('(')[0]  # strip explanations in ()
                res.append(name)
        return res


def lemmas_starts_with(lemmas: List[str], pattern: List[str])->bool:
    pattern_len = len(pattern)
    for a, b in zip_longest(lemmas[:pattern_len], pattern):
        if a!=b:
            return False
    return True


def load_annotation(entity: str) -> Optional[Annotation]:
    anno_filename = entity + '.anno'
    if not os.path.isfile(anno_filename):
        print(f"Annotated file not found. Please, take '{entity + '.cache'}', copy it to '{anno_filename}'"
              f" and annotate it, using '{_start_tag}' and '{_finish_tag}'")
        return None

    with open(anno_filename, 'rt', encoding='utf-8') as f:
        annotation = f.read()
    text = annotation.replace(_start_tag, '').replace(_finish_tag, '')
    res: Annotation = Annotation(text=text)
    cur_pos = 0
    pos_decrement = 0
    start_tag_len = len(_start_tag)
    finish_tag_len = len(_finish_tag)
    while True:
        start = annotation.find(_start_tag, cur_pos)
        if start == -1: break
        s = start - pos_decrement
        pos_decrement += start_tag_len
        cur_pos = start + start_tag_len
        finish = annotation.find(_finish_tag, cur_pos)
        if finish == -1:
            raise ValueError(f"Could not find closing tag after found in position {cur_pos}.")
        f = finish - pos_decrement
        pos_decrement += finish_tag_len
        cur_pos = finish + finish_tag_len
        res.entries.append(Entry(start=s, finish=f))
    return res


def retrieve_wiki_page(entity: str) -> str:
    cache_filename = entity + '.cache'
    if os.path.isfile(cache_filename):
        with open(cache_filename, 'rt', encoding='utf-8') as f:
            content = f.read()
        print(f"Cache file '{cache_filename}' is used.")
        return content

    try:
        page = wikipedia.page(entity)
        content = page.content
        with open(cache_filename, 'wt', encoding='utf-8') as f:
            f.write(content)
            print(f'Wikipedia page "{entity}" content has been stored into file "{cache_filename}"')
        return content
    except wikipedia.exceptions.DisambiguationError:
        print("disambiguation error occurred : " + entity)
    except Exception as ex:
        print("exception occurred for entity: " + entity)
        print(ex)
    return ''


def show_difference(content, annotation):
    for i, (line1, line2) in enumerate(zip_longest(content.splitlines(), annotation.text.splitlines())):
        if line1 != line2:
            print(f"The first difference found in line {i}:")
            print(line1)
            print(line2)
            return


def find_writings2(content: str, checker: Checker) -> Annotation:
    res = Annotation(content)
    doc = _nlp(content)
    for ne in doc.ents:
        if checker.check(str(ne)):
            res.entries.append(Entry(ne.start_char, ne.end_char))
    return res


def find_writings(content: str, checker: Checker) -> Annotation:
    res = Annotation(content)
    doc = _nlp(content)
    max_len = checker.max_len()
    for sent in doc.sents:
        sent_lemmas = [w.lemma_.casefold() for w in sent]
        sent_len = len(sent_lemmas)
        for p in range(0, sent_len):
            for l in range(1, max_len + 1):
                finish_token = p + l
                if finish_token > sent_len:
                    break
                suspect = sent_lemmas[p:finish_token]
                if checker.check_with_order(suspect):
                    start = sent[p].idx
                    finish = sent[finish_token-1].idx + len(sent[finish_token-1])
                    res.entries.append(Entry(start, finish))
    return res


def compare_with_ground_truth(gt: Annotation, checked: Annotation) -> Dict:
    res = {}
    total_in_gt = len(gt.entries)
    total_in_checked = len(checked.entries)
    gt_entries_set = set(str(e.start) + '_' + str(e.finish) for e in gt.entries)
    checked_entries_set = set(str(e.start) + '_' + str(e.finish) for e in checked.entries)
    tp = len(gt_entries_set.intersection(checked_entries_set))
    fp = len(checked_entries_set) - tp
    fn = len(gt_entries_set) - tp
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)
    return {
        'total_in_gt': total_in_gt,
        'total_in_checked': total_in_checked,
        'tp': tp,
        'fp': fp,
        'fn': fn,
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }


def main():
    entity = 'Poul Anderson'
    content: str = retrieve_wiki_page(entity)
    if not content:
        return

    manual_annotation = load_annotation(entity)
    if not manual_annotation:
        return
    if content != manual_annotation.text:
        print('Annotation content is differ from Wikipedia text.')
        show_difference(content, manual_annotation)
        return
    print(f"Annotated entries number: {len(manual_annotation.entries)}")
    for e in manual_annotation.entries:
        print(content[e.start:e.finish])

    print('-' * 64)

    checker = Checker('sparql.tsv')
    auto_annotation = find_writings(content, checker)
    print(f"Found entries number: {len(auto_annotation.entries)}")
    for e in auto_annotation.entries:
        print(content[e.start:e.finish])

    print('=' * 64)
    for name, value in compare_with_ground_truth(manual_annotation, auto_annotation).items():
        print(f"{name}: {value}")


if __name__ == '__main__':
    main()
