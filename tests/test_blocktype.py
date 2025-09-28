import unittest
from src.blocktype import *

class TestBlockType(unittest.TestCase):
    def match_paragraph(self):
        paragraph = "A simple _paragraph_."
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)

    def test_match_heading(self):
        heading1 = "# A heading 1 example"
        self.assertEqual(block_to_block_type(heading1), BlockType.HEADING)

        heading6 = "###### A heading 6 example"
        self.assertEqual(block_to_block_type(heading6), BlockType.HEADING)
        
    def test_match_code(self):
        code = """```
print('hello world!')
```
"""
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_match_quote(self):
        quote = ">This is an example quote."
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
    
    def test_match_unordered_list(self):
        unordered_list = "- An unordered list item."
        self.assertEqual(block_to_block_type(unordered_list), BlockType.UNORDERED_LIST)
    
    def test_match_ordered_list(self):
        ordered_list = "1. A ordered list item."
        self.assertEqual(block_to_block_type(ordered_list), BlockType.ORDERED_LIST)