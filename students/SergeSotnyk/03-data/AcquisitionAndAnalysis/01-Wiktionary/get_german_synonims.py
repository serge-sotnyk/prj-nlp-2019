from prjnlp_utils import download_with_progress
import os

link_uri: str = \
    'https://dumps.wikimedia.org/dewiktionary/20190301/dewiktionary-20190301-pages-articles-multistream.xml.bz2'
filename: str = os.path.join(os.path.dirname(__file__),
                             'data/dewiktionary - 20190301 - pages - articles - multistream.xml.bz2')

if __name__ == '__main__':
    download_with_progress(link_uri, filename)
