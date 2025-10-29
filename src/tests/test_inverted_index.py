import unittest
from src.indexer.inverted_index import InvertedIndex

class TestInvertedIndex(unittest.TestCase):

    def setUp(self):
        self.index = InvertedIndex()

    def test_add_term(self):
        self.index.add_term("test", 1)
        self.assertIn("test", self.index.index)
        self.assertEqual(self.index.index["test"], {1})

    def test_add_term_multiple_documents(self):
        self.index.add_term("test", 1)
        self.index.add_term("test", 2)
        self.assertEqual(self.index.index["test"], {1, 2})

    def test_get_documents(self):
        self.index.add_term("test", 1)
        self.index.add_term("example", 2)
        self.assertEqual(self.index.get_documents("test"), {1})
        self.assertEqual(self.index.get_documents("example"), {2})

    def test_get_documents_nonexistent_term(self):
        self.assertEqual(self.index.get_documents("nonexistent"), set())

if __name__ == '__main__':
    unittest.main()