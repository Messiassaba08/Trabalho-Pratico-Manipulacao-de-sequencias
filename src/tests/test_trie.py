import unittest
from src.indexer.trie import TrieCompact


class TestTrieCompact(unittest.TestCase):

    def setUp(self):
        self.trie = TrieCompact()

    def test_insert_and_get_postings_basic(self):
        self.trie.insert("hello", "doc1", 1)
        self.trie.insert("hello", "doc2", 2)
        self.trie.insert("world", "doc3", 1)

        postings_hello = self.trie.get_postings("hello")
        postings_world = self.trie.get_postings("world")
        postings_none = self.trie.get_postings("notfound")

        self.assertEqual(postings_hello.get("doc1"), 1)
        self.assertEqual(postings_hello.get("doc2"), 2)
        self.assertEqual(postings_world.get("doc3"), 1)
        self.assertEqual(postings_none, {})

    def test_compacted_edges_split_and_merge_paths(self):
        # Insere termos com prefixos comuns para exercitar splits em arestas
        self.trie.insert("compress", "d1", 1)
        self.trie.insert("company", "d2", 1)
        self.trie.insert("comparison", "d3", 1)

        # Todos devem ser recuperáveis exatamente, sem prefix matching parcial
        self.assertIn("d1", self.trie.get_postings("compress"))
        self.assertIn("d2", self.trie.get_postings("company"))
        self.assertIn("d3", self.trie.get_postings("comparison"))
        self.assertEqual(self.trie.get_postings("comp"), {})  # não é termo completo

    def test_empty_term_handling(self):
        # Inserção de string vazia não deve quebrar e não cria termo
        self.trie.insert("", "d1", 1)
        self.assertEqual(self.trie.get_postings(""), {})


if __name__ == '__main__':
    unittest.main()