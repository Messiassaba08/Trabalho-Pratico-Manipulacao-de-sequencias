from typing import List, Set

def evaluate_postings_for_term(index, term):
    postings = index.get_postings(term)
    return set(postings.keys())

def docs_for_ast(index, ast):
    if ast is None:
        return set()
    from ri.query_parser import Term, And, Or
    if isinstance(ast, Term):
        return evaluate_postings_for_term(index, ast.term)
    if isinstance(ast, And):
        left = docs_for_ast(index, ast.left)
        right = docs_for_ast(index, ast.right)
        return left & right
    if isinstance(ast, Or):
        left = docs_for_ast(index, ast.left)
        right = docs_for_ast(index, ast.right)
        return left | right
    return set()

def score_docs(index, query_terms: List[str], candidate_docs: Set[str]):
    scores = {}
    for doc in candidate_docs:
        zs = []
        for term in query_terms:
            z = index.zscore_for(term, doc)
            zs.append(z)
        scores[doc] = sum(zs) / len(zs) if zs else 0.0
    return scores

def calculate_relevance(document, query_terms, corpus):
    relevance_score = 0
    term_frequencies = {term: document.count(term) for term in query_terms}
    total_terms = sum(term_frequencies.values())

    if total_terms > 0:
        for term, freq in term_frequencies.items():
            avg_freq = corpus.get_average_frequency(term)
            z_score = (freq - avg_freq) / avg_freq if avg_freq > 0 else 0
            relevance_score += z_score

    return relevance_score / len(query_terms) if query_terms else 0


def rank_documents(documents, query_terms, corpus):
    ranked_documents = []
    for doc_id, document in documents.items():
        relevance = calculate_relevance(document, query_terms, corpus)
        ranked_documents.append((doc_id, relevance))

    ranked_documents.sort(key=lambda x: x[1], reverse=True)
    return ranked_documents