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
            is_correct_word = ':' not in content
            if is_correct_word:
                self.current_word = content

        elif self.current_tag == "text" and self.is_text_first_line:
            self.is_text_first_line = False

        elif self.current_tag == "text" and is_synonym_start:
            self.is_synonym_ongoing = True

        elif self.current_tag == "text" and self.is_synonym_ongoing and ('*' in content):
            if '[[' in content and ']]' in content:
                content = content.split('[[')[1]
                content = content.split(']]')[0]
                if '#' in content:
                    content = content.split('#')[0]
                self.current_part_synonyms.append(content)

        elif self.current_tag == "text" and self.is_synonym_ongoing:
            self.is_synonym_ongoing = False
            if self.current_part_synonyms:
                self.current_synonyms.append(self.current_part_synonyms)
            self.current_part_synonyms = []


def _write_parsed(inp: dict):
    with open('./data/synonyms_result', 'w') as f:
        for key, value in inp.items():
            inner = ['[' + ', '.join(v) + ']' for v in value]
            result = '{}: [{}]\n'.format(key, ', '.join(inner))
            f.write(result)


if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    handler = WikiHandler()
    parser.setContentHandler(handler)

    parser.parse("./data/frwiktionary-20190301-pages-meta-current.xml")
    print('Total words processed: {}'.format(len(handler.result)))

    _write_parsed(handler.result)
