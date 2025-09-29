import unittest
from src.nodes.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode(
            props={"href": "https://www.example.com", "style": "color=red"}
        )
        html_attrs = html_node.props_to_html()
        self.assertEqual(
            html_attrs, ' href="https://www.example.com" style="color=red"'
        )

