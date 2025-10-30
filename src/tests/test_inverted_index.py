import os
import shutil
import tempfile
import unittest
from src.indexer.inverted_index import InvertedIndex


class TestInvertedIndex(unittest.TestCase):

    def setUp(self):
        # Cria um corpus temporário com alguns arquivos
        self.tempdir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tempdir, 'cat'), exist_ok=True)
        os.makedirs(os.path.join(self.tempdir, 'dog'), exist_ok=True)

        with open(os.path.join(self.tempdir, 'cat', '001.txt'), 'w', encoding='utf-8') as f:
            f.write("Cat cat jumps over mat. Cat likes milk.")
        with open(os.path.join(self.tempdir, 'dog', '002.txt'), 'w', encoding='utf-8') as f:
            f.write("Dog runs fast. Dog chases cat.")

        self.index = InvertedIndex()
        self.index.build_from_corpus(self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_postings_and_frequencies(self):
        postings_cat = self.index.get_postings('cat')
        postings_dog = self.index.get_postings('dog')
        # doc_ids são caminhos relativos como "cat/001.txt" e "dog/002.txt"
        self.assertIn('cat/001.txt', postings_cat)
        self.assertIn('dog/002.txt', postings_dog)
        self.assertGreaterEqual(postings_cat['cat/001.txt'], 1)
        self.assertGreaterEqual(postings_dog['dog/002.txt'], 1)

    def test_doc_lengths(self):
        # Deve conter comprimentos de documentos
        self.assertIn('cat/001.txt', self.index.doc_lengths)
        self.assertIn('dog/002.txt', self.index.doc_lengths)
        self.assertGreater(self.index.get_doc_length('cat/001.txt'), 0)

    def test_zscore_defined(self):
        # zscore deve retornar float, mesmo que std=0 (0.0)
        z = self.index.zscore_for('cat', 'cat/001.txt')
        self.assertIsInstance(z, float)


if __name__ == '__main__':
    unittest.main()