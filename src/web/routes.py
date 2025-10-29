from flask import Blueprint, render_template_string, request, current_app, url_for
from ri.query_parser import parse_query, extract_terms
from ri.ranking import docs_for_ast, score_docs

main = Blueprint('main', __name__)

BASE_HTML = """
<h2>BBC Search Engine</h2>
<form action="{{ url_for('main.search') }}" method="get">
  <input type="text" name="q" value="{{ q|default('') }}" size="60"/>
  <button type="submit">Buscar</button>
</form>
<hr>
{{ body|safe }}
"""

@main.route('/')
def index():
    return render_template_string(BASE_HTML, body="<p>Use AND, OR (maiúsculos) e parênteses. Ex: (casa AND piscina) OR praia</p>")

@main.route('/search')
def search():
    q = request.args.get('q', '').strip()
    page = int(request.args.get('page', '1') or 1)
    per_page = 10
    if not q:
        return render_template_string(BASE_HTML, q=q, body="<p>Sem consulta (use ?q=termo)</p>")

    try:
        ast = parse_query(q)
    except Exception as e:
        return render_template_string(BASE_HTML, q=q, body=f"<p>Erro ao parsear consulta: {e}</p>")

    query_terms = extract_terms(ast)
    index = current_app.indexer

    candidate_docs = docs_for_ast(index, ast)

    if not candidate_docs:
        return render_template_string(BASE_HTML, q=q, body=f"<p>Sem resultados para '{q}'</p>")

    scores = score_docs(index, query_terms, candidate_docs)
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    total = len(sorted_docs)
    start = (page - 1) * per_page
    end = start + per_page
    page_docs = sorted_docs[start:end]

    lines = [f"<p>Resultados {start+1}-{min(end,total)} de {total} (consulta: <b>{q}</b>)</p><ol start='{start+1}'>"]
    for doc_id, score in page_docs:
        best_term = None
        best_z = float('-inf')
        for term in query_terms:
            posting = index.get_postings(term)
            freq = posting.get(doc_id, 0)
            if freq > 0:
                z = index.zscore_for(term, doc_id)
                if z > best_z:
                    best_z = z
                    best_term = term
        if best_term is None:
            best_term = query_terms[0] if query_terms else ''
        snippet = index.snippet_for(doc_id, best_term)
        lines.append(f"<li><b>{doc_id}</b> — score={score:.4f}<br>{snippet}</li>")

    lines.append("</ol>")

    nav = ""
    if start > 0:
        prev_url = url_for('main.search') + f"?q={request.args.get('q')}&page={page-1}"
        nav += f'<a href="{prev_url}">&laquo; anterior</a> '
    if end < total:
        next_url = url_for('main.search') + f"?q={request.args.get('q')}&page={page+1}"
        nav += f'<a href="{next_url}">próxima &raquo;</a>'
    if nav:
        lines.append(f"<div>{nav}</div>")

    body = "\n".join(lines)
    return render_template_string(BASE_HTML, q=q, body=body)