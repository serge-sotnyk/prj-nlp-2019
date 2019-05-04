import os
from collections import namedtuple, defaultdict
from typing import List, Set, Dict

from prjnlp_utils import download_with_progress

Correction = namedtuple('Correction', ['start', 'finish', 'err_type', 'new_text', 'annotator_id'])


class SentInfo:
    def __init__(self,
                 sentence: str = '',
                 annotators_num: int = 0,
                 corrections: List[Correction] = None):
        self.sentence: str = sentence
        self.annotators_num: int = annotators_num
        self.corrections: List[Correction] = corrections if corrections else []


def parse_corrections(annotations: List[str]) -> List[Correction]:
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
        sent = s[2:].strip()
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


link_uri: str = 'https://github.com/andabi/deep-text-corrector/' \
                'raw/master/data/conll14st-test-data/alt/official-2014.combined-withalt.m2'
m2_name: str = os.path.join(os.path.dirname(__file__),
                            'data/official-2014.combined-withalt.m2')
log_name: str = os.path.join(os.path.dirname(__file__),
                            'data/log.txt')


def count_annotators_num(sent_info: SentInfo)->int:
    ids: Set[int] = set()
    for ci in sent_info.corrections:
        ids.add(ci.annotator_id)
    return max(3, len(ids))


def collect_corrections_by_pos(corrections: List[Correction])->Dict[str, List[Correction]]:
    res = defaultdict(list)
    for c in corrections:
        if c.err_type=='noop': # it is not real mistake
            continue
        key_pos = f"{c.start}_{c.finish}"
        res[key_pos].append(c)
    return res


CheckInfo = namedtuple("CheckInfo", 'log total agreed_by_pos agreed_by_type')


def check_sentence(sent_info: SentInfo)->CheckInfo:
    log = ['S ' + sent_info.sentence, ""]

    annotator_num = count_annotators_num(sent_info)
    sent_info.annotators_num = annotator_num
    majority_threshold = annotator_num / 2.0
    agreed_by_pos = 0
    agreed_by_type = 0
    collected_corrections = collect_corrections_by_pos(sent_info.corrections)
    for pos, corrections_in_pos in collected_corrections.items():
        if len(corrections_in_pos) > majority_threshold:
            agreed_by_pos += 1
        error_types = defaultdict(int)
        for c in corrections_in_pos:
            error_types[c.err_type] += 1
        max_corrections_by_type = max(v for k, v in error_types.items())
        if max_corrections_by_type > majority_threshold:
            agreed_by_type += 1
    log.append(f'Annotators assumed: {annotator_num} (agreement threshold = {majority_threshold})')
    log.append(f'Total corrections: {len(collected_corrections)}')
    log.append(f'Agreed by pos: {agreed_by_pos}')
    log.append(f'Agreed by type: {agreed_by_type}')

    res = CheckInfo(log='\n'.join(log),
                    total=len(collected_corrections),
                    agreed_by_pos=agreed_by_pos,
                    agreed_by_type=agreed_by_type)
    return res


if __name__ == '__main__':
    download_with_progress(link_uri, m2_name)
    sent_infos = parce_m2(m2_name)
    print(f"{len(sent_infos)} sentences found.")

    checks = [check_sentence(si) for si in sent_infos]

    total_corrections = sum(c.total for c in checks)
    total_agreed_by_pos = sum(c.agreed_by_pos for c in checks)
    total_agreed_by_type = sum(c.agreed_by_type for c in checks)

    print(f"Total corrections: {total_corrections}")
    print(f"Total corrections agreed by position: {total_agreed_by_pos}")
    print(f"Total corrections agreed by type: {total_agreed_by_type}")

    with open(log_name, 'wt', encoding='utf-8') as lf:
        lf.write('\n\n\n'.join(check.log for check in checks))
    print(f'Detailed log can be found in file "{log_name}"')
