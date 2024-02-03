class HTML_ELEMENT:
    def __init__(self, tag, attributes=None):
        self.tag = tag
        self.attributes = attributes if attributes else {}
        self.children = []
        self.content = ''
    
    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return self.render()

    def render(self, indent=0):
        result = ''
        indent_str = ' ' * indent
        for child in self.children:
            result += f"{indent_str}<{child.tag}"
            for key, value in child.attributes.items():
                result += f' {key}="{value}"'
            result += '>\n'
            result += child.render(indent + 2)
            result += f"{indent_str}</{child.tag}>\n"
        return result
    
    def get_element_attributes(self):
        result = []
        for child in self.children:
            if child.attributes:
                result.append(child.attributes)
            result = [*result, *child.get_element_attributes()]
        return result
    
class HTML_Parser:
    @staticmethod
    def parse_element(element_str):
        tag_start = element_str.find('<') + 1
        tag_end = element_str.find(' ') if ' ' in element_str else len(element_str) - 1
        tag = element_str[tag_start:tag_end]

        attributes = {}
        attribute_str = element_str[tag_end + 1:element_str.find('>')]
        for attribute in attribute_str.split(' '):
            if '=' in attribute:
                key, value = attribute.split('=')
                attributes[key] = value.strip('"')

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
            if char == '<':
                if current:
                    stack.append(current)
                current = char
            elif char == '>':
                current += char
                if current.startswith('</'):
                    parent = stack.pop()
                    current = parent
                else:
                    element = parser.parse_element(current)
                    if stack:
                        stack[-1].add_child(element)
                    else:
                        self.add_child(element)
                    current = element
            else:
                if isinstance(current, HTML_ELEMENT):
                    current.content += char
                else:
                    current += char