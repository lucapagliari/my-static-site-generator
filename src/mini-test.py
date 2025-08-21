from htmlnode import HTMLNode

sample_prop = {}
sample_prop["href"] = "https://www.google.com"
sample_prop["target"] = "_blank"

sample_node = HTMLNode(props=sample_prop)
print(sample_node)
print(sample_node.props_to_html())
#HTMLNode(sample_prop).props_to_html()