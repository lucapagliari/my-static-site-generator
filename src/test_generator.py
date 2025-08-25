import unittest

from website_builder import extract_title

class TestGenerator(unittest.TestCase):

    def test_extract_title(self):
        self.assertEqual(
            extract_title("# Hello"),
            "Hello"
        )
    
    def test_extract_title_exception(self):
        with self.assertRaises(Exception) as cm:
            extract_title("Not a header")