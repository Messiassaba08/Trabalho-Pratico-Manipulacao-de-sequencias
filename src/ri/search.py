from .query_parser import parse_query, extract_terms
from .ranking import docs_for_ast, score_docs

def perform_search(query, inverted_index):
    """
    Executa a busca booleana percorrendo a AST e ranqueia os resultados.

    Critérios:
    - Conectivos: AND = interseção, OR = união (via docs_for_ast)
    - Relevância: média dos z-scores dos termos da consulta (via score_docs)
    Retorna: lista de tuplas (doc_id, score) ordenada por score desc.
    """
    ast = parse_query(query)
    if ast is None:
        return []

    # Documentos candidatos que satisfazem a expressão booleana
    candidate_docs = docs_for_ast(inverted_index, ast)
    if not candidate_docs:
        return []

    # Termos únicos da consulta (em ordem) para cálculo da média de z-scores
    query_terms = extract_terms(ast)

    # scores: média dos z-scores por documento
    scores = score_docs(inverted_index, query_terms, candidate_docs)

    # Ordena por score desc e devolve lista [(doc_id, score), ...]
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)