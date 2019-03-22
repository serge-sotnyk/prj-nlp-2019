import os
import sys
sys.path.append(os.path.realpath(__file__))

from prjnlp_utils import download_with_progress
from m2_parcer import parce_m2


link_uri: str = 'https://github.com/andabi/deep-text-corrector/' \
                'raw/master/data/conll14st-test-data/alt/official-2014.combined-withalt.m2'
m2_name: str = os.path.join(os.path.dirname(__file__),
                            'data/official-2014.combined-withalt.m2')

if __name__ == '__main__':
    download_with_progress(link_uri, m2_name)
    sent_infos = parce_m2(m2_name)
    print(f"{len(sent_infos)} sentences found.")

