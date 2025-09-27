import unittest
from src.process import *
from src.textnode import *

class TestProcess(unittest.TestCase):
    def test_apostrophe(self):
        node = TextNode("This is a text with a `code block` word", TextType.PLAIN)
        new_nodes = split_textnodes_delimiter([node], "`", TextType.CODE)
        expected_output = [
            TextNode("This is a text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_multiple_nodes(self):
        node1 = TextNode("This is a text with a `code block` word", TextType.PLAIN)
        node2 = TextNode("This is a text with a `second code block`", TextType.PLAIN)
        new_nodes = split_textnodes_delimiter([node1, node2,], "`", TextType.CODE)
        expected_output = [
            TextNode("This is a text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
            TextNode("This is a text with a ", TextType.PLAIN),
            TextNode("second code block", TextType.CODE)
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_bold(self):
        node = TextNode("This is a text with a **bold style** word", TextType.PLAIN)
        new_nodes = split_textnodes_delimiter([node], "**", TextType.BOLD)
        expected_output = [
            TextNode("This is a text with a ", TextType.PLAIN),
            TextNode("bold style", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected_output)