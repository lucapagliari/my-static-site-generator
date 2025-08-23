import re
from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        
        splitted = node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise Exception("invalid format: closing delimiter not found")
        
        for i in range(0,len(splitted)):
            if splitted[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text=splitted[i],text_type=TextType.TEXT))
            else:
                new_nodes.append(TextNode(text=splitted[i],text_type=text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        if images is None:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        for image_alt, image_link in images:
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0],text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=image_alt,text_type=TextType.IMAGE,url=image_link))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(text=original_text,text_type=TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        
        links = extract_markdown_links(node.text)
        if links is None:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        for link_name, link_url in links:
            sections = original_text.split(f"[{link_name}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0],text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=link_name,text_type=TextType.LINK,url=link_url))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(text=original_text,text_type=TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)