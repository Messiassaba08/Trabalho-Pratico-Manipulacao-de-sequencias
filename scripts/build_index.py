import os
import sys

# Adiciona o diretório raiz ao path para permitir imports relativos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.indexer.inverted_index import InvertedIndex

def build_inverted_index(corpus_directory, index_file):
    """
    Constrói (ou carrega) o índice invertido usando o método load_or_build.
    
    Esta função delega toda a lógica de indexação para a classe InvertedIndex,
    que é responsável por:
    - Tokenizar o texto usando regex (TOKEN_RE)
    - Construir o índice invertido (term -> {doc_id: freq})
    - Construir a Trie compacta para autocomplete
    - Calcular estatísticas (mean, stddev) para z-scores
    - Persistir o índice em formato JSON
    """
    # Cria a instância do índice invertido
    inverted_index = InvertedIndex()
    
    # load_or_build carrega o índice se existir, ou constrói do zero se não existir
    # Após construir, automaticamente salva o índice no arquivo especificado
    inverted_index.load_or_build(index_file, corpus_directory)
    
    print(f"Índice construído com sucesso!")
    print(f"Total de documentos: {len(inverted_index.doc_ids)}")
    print(f"Total de termos únicos: {len(inverted_index.index)}")
    print(f"Índice salvo em: {index_file}")

if __name__ == '__main__':
    # Define os caminhos relativos ao diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    corpus_dir = os.path.join(project_root, 'data', 'bbc')
    index_file_path = os.path.join(project_root, 'data', 'index', 'inverted_index.json')
    
    # Cria o diretório de índice se não existir
    os.makedirs(os.path.dirname(index_file_path), exist_ok=True)
    
    print(f"Corpus: {corpus_dir}")
    print(f"Índice: {index_file_path}")
    print("Iniciando construção do índice...")
    
    build_inverted_index(corpus_dir, index_file_path)