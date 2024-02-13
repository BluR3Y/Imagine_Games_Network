import re

class HTML_ELEMENT:
    def __init__(self, tag, attributes=None):
        self.tag = tag
        self.attributes = attributes if attributes else {}
        self.children = []
        self.content = ''
    
    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return self.render_document()

    def render_element(self, indent=0):
        attributes_str = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])
        html_element_str = f'<{self.tag} {attributes_str}></{self.tag}>'
        return html_element_str
    
    def render_document(self):
        result = ''
        for child in self.children:
            result += "<" + child.tag
            for key, value in child.attributes.items():
                result += f" {key}=\"{value}\""
            result += '>' + child.content
            result += child.render_document()
            result += f"</{child.tag}>"
        return result
    
    def get_element_attributes(self):
        result = []
        for child in self.children:
            if child.attributes:
                result.append(child.attributes)
            result = [*result, *child.get_element_attributes()]
        return result
    
    def get_elements_by_tag(self, tag):
        elements = []
        for child in self.children:
            if child.tag == tag:
                elements.append(child)
            elements = [*elements, *child.get_elements_by_tag(tag)]
        return elements

class HTML_Parser:
    @staticmethod
    def parse_element(element_str):
        tag_start = element_str.find('<') + 1
        tag_end = element_str.find(' ') if ' ' in element_str else len(element_str) - 1
        tag = element_str[tag_start:tag_end]

        attributes = {}
        attribute_str = element_str[tag_end + 1:element_str.find('>')]
        attribute_regex = re.compile(r'([a-zA-Z0-9\-]+)\s*=\s*(".*?"|\'.*?\'|[^\s>]+)')
        matches = attribute_regex.findall(attribute_str)
        for key, value in matches:
            attributes[key] = value.strip('"\'')

        return HTML_ELEMENT(tag, attributes)

class HTML_DOCUMENT(HTML_ELEMENT):
    def __init__(self, document):
        super().__init__('document')
        self.parse(document)

    def parse(self, document):
        stack = []
        current = None
        parser = HTML_Parser()

        for char in document:
            if isinstance(current, HTML_ELEMENT):
                if char == '<':
                    stack.append(current)
                    current = char
                else:
                    current.content += char
            elif isinstance(current, str):
                current += char
                if char == '>':
                    if current.startswith('</'):
                        current = stack.pop()
                    else:
                        element = parser.parse_element(current)
                        if stack:
                            stack[-1].add_child(element)
                        else:
                            self.add_child(element)
                        current = element
            else:
                current = char