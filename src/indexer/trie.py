from typing import Dict


class TrieNode:
    def __init__(self):
        # Edges compactados: rótulo (string) -> filho
        self.edges: Dict[str, TrieNode] = {}
        self.is_end: bool = False
        self.postings: Dict[str, int] = {}  # doc_id -> freq


class TrieCompact:
    """
    Implementação de Trie compacta (Radix/Patricia) com a mesma API pública:
      - insert(term: str, doc_id: str, freq: int = 1)
      - get_postings(term: str) -> dict

    As arestas armazenam substrings (rótulos) em vez de um caractere por nó.
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
            # Procura uma aresta com prefixo em comum
            for label, child in list(node.edges.items()):
                k = self._common_prefix(rest, label)
                if k == 0:
                    continue
                # Caso 1: o prefixo comum é menor que o label: split da aresta
                if k < len(label):
                    # Divide a aresta existente
                    suffix_existing = label[k:]
                    new_parent = TrieNode()
                    # Reencaminha a aresta existente para o novo nó
                    new_parent.edges[suffix_existing] = child
                    new_parent.is_end = False
                    # Substitui a aresta antiga pelo prefixo comum
                    node.edges.pop(label)
                    node.edges[label[:k]] = new_parent
                    child = new_parent
                    label = label[:k]
                # Agora label é prefixo completo de rest
                rest = rest[k:]
                if not rest:
                    # O termo termina exatamente neste nó/aresta
                    child.is_end = True
                    child.postings[doc_id] = child.postings.get(doc_id, 0) + freq
                    return
                # Se ainda resta sufixo do termo, precisamos continuar descendo
                node = child
                # Tenta encontrar uma aresta cujo label comece com o próximo char de rest
                # Se não existir, cria uma nova aresta com todo o restante
                for next_label in node.edges.keys():
                    if next_label and next_label[0] == rest[0]:
                        break
                else:
                    # Não existe aresta com o próximo caractere, cria uma nova
                    new_child = TrieNode()
                    new_child.is_end = True
                    new_child.postings[doc_id] = new_child.postings.get(doc_id, 0) + freq
                    node.edges[rest] = new_child
                    return
                # Se existir, voltamos ao while para tentar casar novamente (loop externo)
                break
            else:
                # Nenhuma aresta tem prefixo em comum: cria uma nova aresta completa
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
                    # Consumimos todo o termo; só é match se o termo termina exatamente
                    # no final de uma aresta e o nó filho é terminal ou o rótulo também 
                    # é exatamente igual ao resto consumido
                    if k == len(label):
                        # Chegamos ao nó de destino
                        return dict(child.postings) if child.is_end else {}
                    else:
                        # O termo terminou no meio da aresta: não representa um termo completo
                        return {}
                if k < len(label):
                    # O termo diverge no meio da aresta: não há match
                    return {}
                # label é prefixo de rest, seguimos descendo
                rest = rest[k:]
                node = child
                found = True
                break
            if not found:
                # Não existe aresta compatível
                return {}