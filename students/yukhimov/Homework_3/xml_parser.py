import xml.sax


class WikiHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.CurrentData = ''

    def startElement(self, tag, attrs):
        self.CurrentData = tag
        if tag == "sinoniem":
            print('startElement Sinoniem')

    def endElement(self, tag):
        if self.CurrentData == "sinoniem":
            print('endElement Sinoniem')
        self.CurrentData = ''

    def characters(self, content):
        with open('wiki_results.txt', "w") as output_file:
            if self.CurrentData == "sinoniem":
                output_file.write(content + '\n')


if __name__ == '__main__':
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = WikiHandler()
    parser.setContentHandler(Handler)
    parser.parse('afwiki-20190320-pages-articles-multistream.xml')
