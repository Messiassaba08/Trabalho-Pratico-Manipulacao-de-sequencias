from .query_parser import parse_query
from .ranking import calculate_relevance
from ..indexer.inverted_index import InvertedIndex

def perform_search(query, inverted_index):
    parsed_query = parse_query(query)
    document_scores = {}

    for term in parsed_query:
        if term in inverted_index:
            for doc_id in inverted_index[term]:
                if doc_id not in document_scores:
                    document_scores[doc_id] = 0
                document_scores[doc_id] += 1  # Increment score for each term found

    # Calculate relevance scores
    relevance_scores = {doc_id: calculate_relevance(score) for doc_id, score in document_scores.items()}
    
    # Sort documents by relevance score in descending order
    sorted_results = sorted(relevance_scores.items(), key=lambda item: item[1], reverse=True)

    return sorted_results