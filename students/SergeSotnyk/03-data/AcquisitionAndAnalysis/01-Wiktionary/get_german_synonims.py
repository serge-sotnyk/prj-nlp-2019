import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import List, Dict

from tqdm.auto import tqdm

from prjnlp_utils import download_with_progress, unpack_bz2

link_uri: str = \
    'https://dumps.wikimedia.org/dewiktionary/20190301/dewiktionary-20190301-pages-articles-multistream.xml.bz2'
archive_name: str = os.path.join(os.path.dirname(__file__),
                                 'data/dewiktionary-20190301-pages-articles-multistream.xml.bz2')
xml_name: str = archive_name.replace('.xml.bz2', '.xml')
syn_name: str = archive_name.replace('.xml.bz2', '.syn.txt')


def _is_valid_article(text: str) -> bool:
    if text and text.find('({{Sprache|Deutsch}})') >= 0:
        if text.find('{{Synonyme}}') >= 0:
            return True
    return False


def _parse_list(text: str) -> List[str]:
    """
    Parses line like "[[Überstamm]], [[Hauptstamm]], [[Stammgruppe]]"

    :param text:
    :return: list of strings for every synonym
    """
    text = text.replace(']], [[', '|').replace('[[', '').replace(']]', '')
    return list([s for s in text.split('|')])


def _retrieve_de_synonyms(text: str) -> List[str]:
    res = []
    start_syn_tag = text.find('{{Synonyme}}')
    if start_syn_tag >= 0:
        start_syn_list = text.find('[[', start_syn_tag)
        if start_syn_list >= 0:
            finish_syn_list = text.find('\n', start_syn_list)
            if finish_syn_list >= 0:
                res = _parse_list(text[start_syn_list:finish_syn_list])
    return res


def parse_wiktionary_stream(stream):
    res = defaultdict(list)

    title: str = ''
    print("Start processing XML.")
    for event, elem in tqdm(ET.iterparse(stream, events=('end',)), unit="nodes"):
        # events=('start', 'end', 'start-ns', 'end-ns')):
        if elem.tag.endswith('}title'):
            title = elem.text
        elif elem.tag.endswith('}text'):
            text = elem.text
            if _is_valid_article(text):
                syn_list = _retrieve_de_synonyms(text)
                if syn_list:
                    res[title] += syn_list
    print("Done!")
    return res


def _write_stat(syn_dict: Dict[str, List[str]]):
    syn_list = list([[k]+v for k, v in syn_dict.items()])
    print(f"Found terms with synonyms: {len(syn_list)}")
    longest_set = max(syn_list, key=len)
    print(f"The longest set has length {len(longest_set)}")
    print(longest_set)
    with open(syn_name, 'w', encoding='utf-8') as outp:
        for synset in syn_list:
            outp.write(str(synset)+'\n')
    print(f"Synonyms has been written into '{syn_name}'")


if __name__ == '__main__':
    download_with_progress(link_uri, archive_name)
    unpack_bz2(archive_name, xml_name)
    with open(xml_name, mode='r', encoding="utf-8") as xml:
        syn_dict = parse_wiktionary_stream(xml)
    _write_stat(syn_dict)
