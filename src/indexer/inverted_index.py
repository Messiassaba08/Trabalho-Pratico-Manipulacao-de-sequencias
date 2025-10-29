class InvertedIndex:
    def __init__(self):
        self.index = {}

    def add_term(self, term, doc_id):
        if term not in self.index:
            self.index[term] = set()
        self.index[term].add(doc_id)

    def get_documents(self, term):
        return self.index.get(term, set())