import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

HEADING_PATTERN = r"^#{1,6} .+"
CODE_PATTERN = r"^`{3}[\s\S]+`{3}$"
QUOTE_PATTERN = r"^>.+"
UNORDERED_LIST_PATTERN = r"^- .+"
ORDERED_LIST_PATTERN = r"^\d\. .+"

def block_to_block_type(block):
    if re.match(HEADING_PATTERN, block):
        return BlockType.HEADING
    elif re.match(CODE_PATTERN, block):
        return BlockType.CODE
    elif re.match(QUOTE_PATTERN, block):
        return BlockType.QUOTE
    elif re.match(UNORDERED_LIST_PATTERN, block):
        return BlockType.UNORDERED_LIST
    elif re.match(ORDERED_LIST_PATTERN, block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
