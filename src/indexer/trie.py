class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.postings = {}  # doc_id -> freq

class TrieCompact:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, term: str, doc_id: str, freq: int = 1):
        node = self.root
        for ch in term:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True
        node.postings[doc_id] = node.postings.get(doc_id, 0) + freq

    def get_postings(self, term: str):
        node = self.root
        for ch in term:
            if ch not in node.children:
                return {}
            node = node.children[ch]
        if node.is_end:
            return dict(node.postings)
        return {}