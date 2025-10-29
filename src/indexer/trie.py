class TrieNode:
    def __init__(self):
        self.children = {}
        self.documents = set()

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, document_id):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.documents.add(document_id)

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return set()
            node = node.children[char]
        return node.documents

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return set()
            node = node.children[char]
        return self._collect_documents(node)

    def _collect_documents(self, node):
        documents = set(node.documents)
        for child in node.children.values():
            documents.update(self._collect_documents(child))
        return documents