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