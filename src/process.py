import re
import os
from .nodes.textnode import TextNode, TextType
from .nodes.parentnode import ParentNode
from .blocktype import block_to_block_type, BlockType

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
            if i % 2 == 0:
                text = text_splits[i // 2]
                if not text:
                    continue
                new_nodes.append(TextNode(text, node.text_type, node.url))
            else:
                new_nodes.append(
                    TextNode(images[i // 2][0], TextType.IMAGE, images[i // 2][1])
                )

    return new_nodes


def split_textnodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        text_splits = re.split(r"\[.*?\]\(.*?\)", node.text)
        links = extract_markdown_links(node.text)
        for i in range(len(text_splits) + len(links)):
            if i % 2 == 0:
                text = text_splits[i // 2]
                if not text:
                    continue
                new_nodes.append(TextNode(text, node.text_type, node.url))
            else:
                new_nodes.append(
                    TextNode(links[i // 2][0], TextType.LINK, links[i // 2][1])
                )

    return new_nodes


def text_to_textnodes(text):
    italicized = split_textnodes_delimiter(
        [TextNode(text, TextType.PLAIN)], "_", TextType.ITALIC
    )
    bolder = split_textnodes_delimiter(italicized, "**", TextType.BOLD)
    code = split_textnodes_delimiter(bolder, "`", TextType.CODE)
    images = split_textnodes_image(code)
    links = split_textnodes_link(images)
    return links


def markdown_to_blocks(markdown):
    return list(
        filter(lambda x: len(x) > 0, map(lambda x: x.strip(), markdown.split("\n\n")))
    )


def create_paragraph(markdown):
    return ParentNode("p", text_to_textnodes(markdown))


def create_heading(markdown):
    return ParentNode("h1", text_to_textnodes(re.sub(r"#{1,6} ", "", markdown)))


def create_code(markdown):
    return ParentNode(
        "pre", [TextNode(re.sub(r"(<br>)?```(<br>)?", "", markdown), TextType.CODE)]
    )


def create_quote(markdown):
    return ParentNode("blockquote", text_to_textnodes(re.sub(r"\B>\s?\B", "", markdown)))


def create_unordered_list(markdown):
    items = markdown.split("\n")
    items_node = []
    for item in items:
        nodes = text_to_textnodes(item.lstrip("- "))
        items_node.append(ParentNode("li", nodes))
    return ParentNode("ul", items_node)


def create_ordered_list(markdown):
    items = markdown.split("\n")
    items_node = []
    for item in items:
        nodes = text_to_textnodes(re.sub(r"\d+\. ", "", item))
        items_node.append(ParentNode("li", nodes))
    return ParentNode("ol", items_node)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_types = list(map(block_to_block_type, blocks))
    body_items = []
    for block, block_type in zip(blocks, block_types):
        if block_type == BlockType.HEADING:
            body_items.append(create_heading(replace_newline_with_br_tag(block)))
        elif block_type == BlockType.CODE:
            body_items.append(create_code(replace_newline_with_br_tag(block)))
        elif block_type == BlockType.QUOTE:
            body_items.append(create_quote(replace_newline_with_br_tag(block)))
        elif block_type == BlockType.UNORDERED_LIST:
            body_items.append(create_unordered_list(block))
        elif block_type == BlockType.ORDERED_LIST:
            body_items.append(create_ordered_list(block))
        else:
            body_items.append(create_paragraph(replace_newline_with_br_tag(block)))
    html_output = ParentNode("body", body_items)
    return html_output


def replace_newline_with_br_tag(text):
    return text.replace("\n", "<br>")


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("# ")

    raise ValueError("No title provided.")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    template = None
    with open(template_path, "r", encoding="utf_8") as f:
        template = f.read()

    markdown_txt = None
    with open(from_path, "r", encoding="utf_8") as f:
        markdown_txt = f.read()

    title = extract_title(markdown_txt)
    generated_html = markdown_to_html_node(markdown_txt).to_html()

    template = template.replace(r"{{ Title }}", title)
    template = template.replace(r"{{ Content }}", generated_html)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf_8") as f:
        f.write(template)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    for (root, dirs, files) in os.walk(dir_path_content, topdown=True):
        for file in files:
            content_path = os.path.join(root, file)
            output_path = os.path.join(root.replace(dir_path_content, dest_dir_path), file.replace("md", "html"))
            generate_page(content_path, template_path, output_path)