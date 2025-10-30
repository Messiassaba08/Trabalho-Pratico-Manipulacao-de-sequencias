from .query_parser import parse_query, extract_terms
from .ranking import docs_for_ast, score_docs

def perform_search(query, inverted_index):
    """Executa a consulta booleana e retorna [(doc_id, score)] ordenado por score."""
    ast = parse_query(query)
    if ast is None:
        return []

    candidate_docs = docs_for_ast(inverted_index, ast)
    if not candidate_docs:
        return []

    query_terms = extract_terms(ast)

    scores = score_docs(inverted_index, query_terms, candidate_docs)

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)