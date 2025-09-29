import unittest
from src.process import *
from src.nodes.textnode import *


class TestProcess(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_output = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected_output, text_to_textnodes(text))

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<body><p>This is <b>bolded</b> paragraph<br>text in a p<br>tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></body>",
        )
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<body><pre><code>This is text that _should_ remain<br>the **same** even with inline stuff</code></pre></body>",
        )

    def test_extract_title(self):
        title = extract_title("# Title")
        self.assertEqual("Title", title)

        title = extract_title("Some text here\n\n# Title 2")
        self.assertEqual("Title 2", title)



class TestSplitTextNodes(unittest.TestCase):
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
        new_nodes = split_textnodes_delimiter(
            [
                node1,
                node2,
            ],
            "`",
            TextType.CODE,
        )
        expected_output = [
            TextNode("This is a text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
            TextNode("This is a text with a ", TextType.PLAIN),
            TextNode("second code block", TextType.CODE),
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

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        expected_output = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(split_textnodes_image([node]), expected_output)

    def test_split_link(self):
        node = TextNode(
            "This is text with an [first link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        expected_output = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("first link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(split_textnodes_link([node]), expected_output)


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is a text with an [Click me!](https://www.example.com)"
        )
        self.assertListEqual([("Click me!", "https://www.example.com")], matches)
