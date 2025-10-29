import unittest
from src.indexer.trie import Trie

class TestTrie(unittest.TestCase):

    def setUp(self):
        self.trie = Trie()

    def test_insert_and_search(self):
        self.trie.insert("hello", 1)
        self.trie.insert("hello", 2)
        self.trie.insert("world", 3)

        self.assertTrue(self.trie.search("hello"))
        self.assertTrue(self.trie.search("world"))
        self.assertFalse(self.trie.search("notfound"))

    def test_search_with_documents(self):
        self.trie.insert("test", 1)
        self.trie.insert("test", 2)

        documents = self.trie.search("test")
        self.assertIn(1, documents)
        self.assertIn(2, documents)

    def test_insert_empty_string(self):
        with self.assertRaises(ValueError):
            self.trie.insert("", 1)

    def test_search_empty_string(self):
        self.assertFalse(self.trie.search(""))

if __name__ == '__main__':
    unittest.main()