from typing import Dict


class TrieNode:
    def __init__(self):
        # Arestas compactadas: rótulo (substring) -> filho
        self.edges: Dict[str, TrieNode] = {}
        self.is_end: bool = False
        self.postings: Dict[str, int] = {}  # doc_id -> frequência


class TrieCompact:
    """Trie compacta (Radix/Patricia) com API:
    - insert(term, doc_id, freq)
    - get_postings(term) -> {doc_id: freq}
    """

    def __init__(self):
        self.root = TrieNode()

    @staticmethod
    def _common_prefix(a: str, b: str) -> int:
        i = 0
        n = min(len(a), len(b))
        while i < n and a[i] == b[i]:
            i += 1
        return i

    def insert(self, term: str, doc_id: str, freq: int = 1):
        if not term:
            return
        node = self.root
        rest = term
        while True:
            # Procura aresta com prefixo em comum
            for label, child in list(node.edges.items()):
                k = self._common_prefix(rest, label)
                if k == 0:
                    continue
                # Split da aresta quando prefixo comum < label
                if k < len(label):
                    suffix_existing = label[k:]
                    new_parent = TrieNode()
                    new_parent.edges[suffix_existing] = child
                    new_parent.is_end = False
                    node.edges.pop(label)
                    node.edges[label[:k]] = new_parent
                    child = new_parent
                    label = label[:k]
                # label é prefixo de rest
                rest = rest[k:]
                if not rest:
                    # Termo completo
                    child.is_end = True
                    child.postings[doc_id] = child.postings.get(doc_id, 0) + freq
                    return
                # Continua descendo
                node = child
                # Se não existir aresta com o próximo caractere, cria nova
                for next_label in node.edges.keys():
                    if next_label and next_label[0] == rest[0]:
                        break
                else:
                    new_child = TrieNode()
                    new_child.is_end = True
                    new_child.postings[doc_id] = new_child.postings.get(doc_id, 0) + freq
                    node.edges[rest] = new_child
                    return
                # Se existir, tenta casar novamente
                break
            else:
                # Sem prefixo em comum: cria aresta com todo o restante
                new_child = TrieNode()
                new_child.is_end = True
                new_child.postings[doc_id] = new_child.postings.get(doc_id, 0) + freq
                node.edges[rest] = new_child
                return

    def get_postings(self, term: str):
        if not term:
            return {}
        node = self.root
        rest = term
        while True:
            found = False
            for label, child in node.edges.items():
                k = self._common_prefix(rest, label)
                if k == 0:
                    continue
                if k == len(rest) and k <= len(label):
                    # Match exato do termo
                    if k == len(label):
                        return dict(child.postings) if child.is_end else {}
                    else:
                        return {}
                if k < len(label):
                    return {}
                # label é prefixo de rest; desce mais
                rest = rest[k:]
                node = child
                found = True
                break
            if not found:
                return {}