from enum import Enum
from src.nodes.leafnode import LeafNode


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode(LeafNode):
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        tag, props = self._text_type_to_html_tag(text_type, url)
        super().__init__(text, tag, props)

    def _text_type_to_html_tag(self, text_type, url):
        match text_type:
            case TextType.PLAIN:
                return (None, None)
            case TextType.BOLD:
                return ("b", None)
            case TextType.ITALIC:
                return ("i", None)
            case TextType.CODE:
                return ("code", None)
            case TextType.LINK:
                return ("a", { "href": url })
            case TextType.IMAGE:
                return ("img", { "src": url })


    def __eq__(self, value):
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
