import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):

    def test_props(self):
        sample_prop = {}
        sample_prop["href"] = "https://www.google.com"
        sample_prop["target"] = "_blank"
        self.assertEqual(HTMLNode(props=sample_prop).props_to_html(),'href="https://www.google.com" target="_blank"')

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )
    
    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

if __name__ == "__main__":
    unittest.main()