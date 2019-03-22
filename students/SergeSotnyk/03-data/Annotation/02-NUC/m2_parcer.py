from collections import namedtuple
from typing import List

Correction = namedtuple('Correction', ['start', 'finish', 'err_type', 'new_text', 'annotator_id'])


class SentInfo:
    def __init__(self,
                 sentence: str = '',
                 corrections: List[Correction] = None):
        self.sentence: str = sentence
        self.corrections = corrections if corrections else []


def parse_corrections(annotations: List[str])->List[Correction]:
    res = []
    for a in annotations:
        if not a.startswith('A '):
            raise ValueError(f'Expected string, started from "A ", but "{a}" found.')
        a = a[2:].strip()
        parts = a.split('|')
        positions = parts[0].split(' ')
        start = int(positions[0])
        finish = int(positions[1])
        err_type = parts[3]
        new_text = parts[6]
        annotator_id = int(parts[-1])
        res.append(Correction(start=start, finish=finish, err_type=err_type,
                              new_text=new_text, annotator_id=annotator_id))
    return res


def try_add_sentinfo(res, ss, a):
    s = ss[0]
    if len(s) > 0 and s.startswith('S '):
        sent = s[2:]
        corrections = parse_corrections(a)
        res.append(SentInfo(sentence=sent, corrections=corrections))
    ss[0] = ''
    a.clear()


def parce_m2(filename: str) -> List[SentInfo]:
    res = []
    with open(filename, 'rt', encoding='utf-8') as f:
        s = ['']  # List with one item to allow clearing it in try_add_sentinfo
        a = []
        for line in f:
            if line.strip() == '':
                try_add_sentinfo(res, s, a)
            elif line.startswith('S '):
                s = [line]
            elif line.startswith('A '):
                a.append(line)
            else:
                raise ValueError(f'Unknown line type: "{line}"')
        try_add_sentinfo(res, s, a)
    return res
