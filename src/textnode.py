from enum import Enum

class TextType(Enum):
    PLAIN = "plain Text"
    BOLD = "bold" 
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None=None):
        self.text = text 
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return (self.text, self.text_type, self.url) == (value.text, value.text_type, value.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
