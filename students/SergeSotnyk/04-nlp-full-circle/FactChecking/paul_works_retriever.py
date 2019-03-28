from itertools import zip_longest
from typing import List, Optional

import wikipedia
import os

_start_tag = '<*'
_finish_tag = '*>'


class Entry:
    def __init__(self, start: int, finish: int):
        self.start = start
        self.finish = finish


class Annotation:
    def __init__(self, text: str = '', entries: List[Entry] = None):
        self.text = text
        self.entries = entries if entries else []


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


def main():
    entity = 'Poul Anderson'
    content: str = retrieve_wiki_page(entity)
    if not content:
        return

    annotation = load_annotation(entity)
    if not annotation:
        return
    if content != annotation.text:
        print('Annotation content is differ from Wikipedia text.')
        show_difference(content, annotation)
        return
    print(f"Annotated entries number: {len(annotation.entries)}")
    for e in annotation.entries:
        print(content[e.start:e.finish])


if __name__ == '__main__':
    main()
