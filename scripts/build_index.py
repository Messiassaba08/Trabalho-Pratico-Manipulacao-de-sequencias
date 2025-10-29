import os
import json
from src.indexer.inverted_index import InvertedIndex
from src.indexer.persistence import save_inverted_index

def build_inverted_index(corpus_directory, index_file):
    inverted_index = InvertedIndex()

    for filename in os.listdir(corpus_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(corpus_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                terms = content.split()  # Simple tokenization
                for term in terms:
                    inverted_index.add_term(term, filename)

    save_index(inverted_index, index_file)

if __name__ == '__main__':
    corpus_dir = 'data/bbc'  # Adjust path as necessary
    index_file_path = '../data/index/inverted_index.dat'  # Adjust path as necessary
    build_inverted_index(corpus_dir, index_file_path)