import os
import sys
import xml.sax

from prjnlp_utils import download_with_progress, unpack_bz2

link_uri: str = \
    'https://dumps.wikimedia.org/dewiktionary/20190301/dewiktionary-20190301-pages-articles-multistream.xml.bz2'
archive_name: str = os.path.join(os.path.dirname(__file__),
                             'data/dewiktionary - 20190301 - pages - articles - multistream.xml.bz2')
file_name: str = archive_name.replace('.xml.bz2', '.xml')


class SynonymHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)  # super constructor
        self.path = []  # do some init

    def getParentElement(self):
        """Return the immediate parent element name."""
        if len(self.path) == 0:
            return None
        return self.path[-1]

    def descendentOf(self, name):
        """Return True if the current path contains the given name."""
        try:
            self.path.index(name)
            return True
        except:
            return False

    def getPathStr(self):
        """Return the path as a string."""
        return '/'.join(self.path)

    def startElement(self, name, attrs):
        """Handle the start of an element and do normal processing."""
        sys.stdout.write('<%s> ' % name)
        sys.stdout.write(' path=%s ' % self.getPathStr())
        sys.stdout.write(' parent=%s ' % self.getParentElement())
        sys.stdout.write(' descOf(emplist)=%s\n' % \
                         self.descendentOf('emplist'))  # normal processing

        self.path.append(name)  # track the path

    def endElement(self, name):
        """Handle the end of the element."""
        self.path.pop()  # track the path


def parse_wiktionary_stream(stream):
    ...


if __name__ == '__main__':
    download_with_progress(link_uri, archive_name)
    unpack_bz2(archive_name, file_name)


