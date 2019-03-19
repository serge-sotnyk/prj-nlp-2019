import xml.sax


# {word: [[synonyms]]}

class WikiHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_tag = ""
        self.is_title = False
        self.is_text_first_line = False
        self.is_synonym_ongoing = False
        self.current_word = ""
        self.current_synonyms = []
        self.current_part_synonyms = []
        self.result = {}

    def startElement(self, tag, attributes):
        self.current_tag = tag
        if tag == "text" and attributes.get('xml:space'):
            self.is_text_first_line = True

    def endElement(self, tag):
        if self.current_synonyms and self.current_word and self.current_tag == "text":
            print('Pushing word {} into result with synonyms {}'.format(self.current_word, len(self.current_synonyms)))
            self.result[self.current_word] = self.current_synonyms
            self.current_word = ""
            self.current_synonyms = []
        self.current_tag = ""

    def characters(self, content):
        content = content.strip()
        if not content:
            return

        is_synonym_start = "synonymes" in content
        if self.current_tag == "title":
            # check no spec-symbols in title
            self.current_word = content
        elif self.current_tag == "text" and self.is_text_first_line:
            self.is_text_first_line = False
        elif self.current_tag == "text" and is_synonym_start:
            self.is_synonym_ongoing = True
        elif self.current_tag == "text" and self.is_synonym_ongoing and ('*' in content):
            # check synonyms are parsed
            self.current_part_synonyms.append(content)
        elif self.current_tag == "text" and self.is_synonym_ongoing:
            self.is_synonym_ongoing = False
            self.current_synonyms.append(self.current_part_synonyms)
            self.current_part_synonyms = []


if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = WikiHandler()
    parser.setContentHandler(Handler)

    parser.parse("./data/frwiktionary-20190301-pages-meta-current.xml")
