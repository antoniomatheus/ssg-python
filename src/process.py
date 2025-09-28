import re
from src.textnode import TextNode

def split_textnodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        for idx, text_split in enumerate(text.split(delimiter)):
            if len(text_split) == 0:
                continue

            if idx % 2 == 0:
                new_nodes.append(TextNode(text_split, node.text_type))
            else:
                new_nodes.append(TextNode(text_split, text_type))
    return new_nodes
        
def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)