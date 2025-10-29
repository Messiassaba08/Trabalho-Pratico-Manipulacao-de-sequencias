def create_snippet(text, term, context=80):
    term_index = text.lower().find(term.lower())
    if term_index == -1:
        return ""

    start_index = max(term_index - context, 0)
    end_index = min(term_index + len(term) + context, len(text))

    snippet = text[start_index:end_index]
    highlighted_snippet = snippet.replace(term, f"<b>{term}</b>")

    return highlighted_snippet