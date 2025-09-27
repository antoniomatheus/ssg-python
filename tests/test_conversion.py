import unittest
from src.conversion import text_node_to_html_node
from src.textnode import TextNode, TextType

class TestTextNodeConversion(unittest.TestCase):
    def test_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")
        html_output = '<b>This is a bold text</b>'
        self.assertEqual(html_node.to_html(), html_output)

    def test_italic(self):
        node = TextNode("This is an italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text")
        html_output = '<i>This is an italic text</i>'
        self.assertEqual(html_node.to_html(), html_output)

    def test_code(self):
        node = TextNode("print('hello world!')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello world!')")
        html_output = "<code>print('hello world!')</code>"
        self.assertEqual(html_node.to_html(), html_output)
    
    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, { "href": "https://www.example.com" })
        html_output = '<a href="https://www.example.com">Click me!</a>'
        self.assertEqual(html_node.to_html(), html_output)

    def test_image(self):
        node = TextNode("An example image", TextType.IMAGE, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        html_output = '<img src="https://www.example.com" alt="An example image"></img>'
        self.assertEqual(html_node.to_html(), html_output)