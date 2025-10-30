import os
import sys

# Adiciona o diretório raiz ao path para permitir imports relativos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.indexer.inverted_index import InvertedIndex

def build_inverted_index(corpus_directory, index_file):
    """Carrega o índice existente ou constrói e salva em JSON."""
    inverted_index = InvertedIndex()
    inverted_index.load_or_build(index_file, corpus_directory)
    print("Índice construído com sucesso!")
    print(f"Total de documentos: {len(inverted_index.doc_ids)}")
    print(f"Total de termos únicos: {len(inverted_index.index)}")
    print(f"Índice salvo em: {index_file}")

if __name__ == '__main__':
    # Caminhos relativos ao diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    corpus_dir = os.path.join(project_root, 'data', 'bbc')
    index_file_path = os.path.join(project_root, 'data', 'index', 'inverted_index.json')
    
    # Garante o diretório de saída
    os.makedirs(os.path.dirname(index_file_path), exist_ok=True)
    
    print(f"Corpus: {corpus_dir}")
    print(f"Índice: {index_file_path}")
    print("Iniciando construção do índice...")
    
    build_inverted_index(corpus_dir, index_file_path)