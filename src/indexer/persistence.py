"""Wrappers de persistência baseados em JSON via InvertedIndex.save/load."""

from .inverted_index import InvertedIndex


def save_inverted_index(index: InvertedIndex, file_path: str) -> None:
    """Salva o índice invertido em formato JSON (texto)."""
    index.save(file_path)


def load_inverted_index(file_path: str) -> InvertedIndex:
    """Carrega o índice invertido a partir de um arquivo JSON (texto)."""
    idx = InvertedIndex()
    idx.load(file_path)
    return idx