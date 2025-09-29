import unittest
from src.nodes.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_without_attributes(self):
        node = LeafNode("Hello World!", "p")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")

    def test_with_attributes(self):
        node = LeafNode("Click me!", "a", {"href": "https://www.example.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.example.com">Click me!</a>'
        )

    def test_without_a_value(self):
        node = LeafNode(None, "p")
        with self.assertRaises(ValueError) as err:
            node.to_html()
        self.assertEqual(str(err.exception), "All leaf nodes must have a value.")