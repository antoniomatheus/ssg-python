import re
from src.textnode import TextNode, TextType

MARKDOWN_IMAGE_PATTERN = r"!\[(.*?)\]\((.*?)\)"
MARKDOWN_LINK_PATTERN = r"\[(.*?)\]\((.*?)\)"

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
    return re.findall(MARKDOWN_IMAGE_PATTERN, text)

def extract_markdown_links(text):
    return re.findall(MARKDOWN_LINK_PATTERN, text)

def split_textnodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        text_splits = re.split(r"!\[.*?\]\(.*?\)", node.text)
        images = extract_markdown_images(node.text)
        for i in range(len(text_splits) + len(images)):
            if (i % 2 == 0):
                text = text_splits[i // 2]
                if not text:
                    continue
                new_nodes.append(TextNode(text, node.text_type, node.url))
            else:
                new_nodes.append(TextNode(images[i // 2][0], TextType.IMAGE, images[i // 2][1]))
    
    return new_nodes

def split_textnodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        text_splits = re.split(r"\[.*?\]\(.*?\)", node.text)
        links = extract_markdown_links(node.text)
        for i in range(len(text_splits) + len(links)):
            if (i % 2 == 0):
                text = text_splits[i // 2]
                if not text:
                    continue
                new_nodes.append(TextNode(text, node.text_type, node.url))
            else:
                new_nodes.append(TextNode(links[i // 2][0], TextType.LINK, links[i // 2][1]))
    
    return new_nodes

def text_to_textnodes(text):
    italicized = split_textnodes_delimiter([TextNode(text, TextType.PLAIN)], "_", TextType.ITALIC)
    bolder = split_textnodes_delimiter(italicized, "**", TextType.BOLD)
    code = split_textnodes_delimiter(bolder, "`", TextType.CODE)
    images = split_textnodes_image(code)
    links = split_textnodes_link(images)
    return links

def markdown_to_blocks(markdown):
    return list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), markdown.split("\n\n"))))