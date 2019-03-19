# import warc
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
# extract individual items,
# perform basic statistical analysis (distribution of hosts, words, languages, domains etc.)
# and visualization (optional).

#
with open('./data/CC-MAIN-20190116031807-20190116053807-00514.warc', 'rb') as stream:
    for record in ArchiveIterator(stream):
        if record.rec_type == 'response':
            content = record.content_stream().read()

            print(record.rec_headers.get_header('WARC-Target-URI'))
            print(record.content_stream().read())

