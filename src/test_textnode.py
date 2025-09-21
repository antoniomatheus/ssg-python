import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        

    def test_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node_text = TextNode("Text not with different text", TextType.BOLD)
        node_type = TextNode("This is a text node", TextType.PLAIN)
        node_url = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node, node_text)
        self.assertNotEqual(node, node_type)
        self.assertNotEqual(node, node_url)

if __name__ == "__main__":
    unittest.main()