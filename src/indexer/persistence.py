"""
Módulo de persistência (atualizado)
----------------------------------

Este módulo foi simplificado para evitar confusão com formatos antigos.
Atualmente, a persistência do índice invertido é feita diretamente pelos
métodos da classe `InvertedIndex`:

  - InvertedIndex.save(path)        -> salva em JSON texto
  - InvertedIndex.load(path)        -> carrega de JSON texto
  - InvertedIndex.load_or_build(...) -> carrega ou constrói e persiste

Para manter compatibilidade mínima, expomos funções auxiliares que 
delegam para a implementação oficial da classe `InvertedIndex`.
"""

from .inverted_index import InvertedIndex


def save_inverted_index(index: InvertedIndex, file_path: str) -> None:
    """Salva o índice invertido em formato JSON (texto)."""
    index.save(file_path)


def load_inverted_index(file_path: str) -> InvertedIndex:
    """Carrega o índice invertido a partir de um arquivo JSON (texto)."""
    idx = InvertedIndex()
    idx.load(file_path)
    return idx