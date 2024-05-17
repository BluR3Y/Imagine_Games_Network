from html.parser import HTMLParser
import html

self_closing_elements = ["area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"]

class HTMLNode:
    def __init__(self, tag):
        self.tag = tag
        self.attributes = {}
        self.children = []  # Stores with inner-text and child elements

    def add_child(self, child):
        self.children.append(child)

    def set_attribute(self, attr, value):
        self.attributes[attr] = value

    def render_element(self, with_children = False):
        result = f"<{self.tag}"
        for key, value in self.attributes.items():
            result += f" {key}=\"{value}\""
        if not self.children and self.tag in self_closing_elements:
            result += " />"
        else:
            result += '>'
            if with_children:
                for child in self.children:
                    if isinstance(child, HTMLNode):
                        result += child.render_element(with_children)
                    else:
                        result += html.escape(child)
            result += f"</{self.tag}>"
        return result

class HTMLDocument(HTMLParser):
    def __init__(self, document):
        super().__init__()
        self.active_stack = []
        self.inactive_stack = []
        self.root_node = None
        self.document = document
        self.feed(document)

    def handle_starttag(self, tag, attrs):
        node = HTMLNode(tag)
        for attr, value in attrs:
            node.set_attribute(attr, value)
        if not self.root_node:
            self.root_node = node
        else:
            self.active_stack[-1].add_child(node)
        self.active_stack.append(node)

    def handle_data(self, data):
        if self.active_stack:
            self.active_stack[-1].add_child(data)

    def handle_endtag(self, tag):
        if self.active_stack and self.active_stack[-1].tag in self_closing_elements and self.active_stack[-1].tag != tag:
            self.inactive_stack.append(self.active_stack.pop())
 
        if len(self.active_stack) == 1 and self.active_stack[0].tag == tag and self.getpos()[1] < len(self.document) - 10 and self.inactive_stack and self.inactive_stack[-1].tag == tag:
            print(f"Warning Invalid Closing Tag {tag}")
        elif not self.active_stack and self.root_node:
            self.active_stack.append(self.root_node)
        elif self.active_stack:
            self.inactive_stack.append(self.active_stack.pop())