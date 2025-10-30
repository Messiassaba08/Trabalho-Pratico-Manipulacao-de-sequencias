from flask import Blueprint, render_template_string, request, current_app, url_for
from ri.query_parser import parse_query, extract_terms
from ri.ranking import docs_for_ast, score_docs
import os

main = Blueprint('main', __name__)

BASE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Buscador</title>
    <style>
        body {
            font-family: "Poppins", "Segoe UI", Roboto, Arial, sans-serif;
            background-color: #fafafa;
            margin: 0;
            padding: 0;
            color: #202124;
        }

        .search-container {
            text-align: center;
            margin-top: 10%;
            position: relative;
        }

        h1 {
            font-size: 58px;
            font-weight: 600;
            background: linear-gradient(90deg, #1a73e8, #4285f4, #34a853);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 25px;
            letter-spacing: -1px;
            text-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        form {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: white;
            padding: 10px 16px;
            border-radius: 40px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            width: 60%;
            max-width: 600px;
            transition: box-shadow 0.2s ease;
        }

        form:hover {
            box-shadow: 0 3px 8px rgba(0,0,0,0.25);
        }

        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: none;
            outline: none;
            font-size: 16px;
        }

        input[type="text"]:focus {
            outline: none;
            box-shadow: none;
        }

        button {
            padding: 10px 18px;
            border: none;
            background: #1a73e8;
            color: #fff;
            border-radius: 24px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 500;
            transition: background 0.2s ease;
        }

        button:hover {
            background: #155ab6;
        }

        .help-icon {
            position: relative;
            display: inline-block;
            font-weight: bold;
            color: #1a73e8;
            cursor: pointer;
            border: 2px solid #1a73e8;
            border-radius: 50%;
            width: 22px;
            height: 22px;
            line-height: 18px;
            text-align: center;
            font-size: 15px;
            user-select: none;
        }

        .help-tooltip {
            visibility: hidden;
            opacity: 0;
            position: absolute;
            top: 40px;
            left: 50%;
            transform: translateX(-50%);
            background: #fff;
            color: #333;
            text-align: left;
            border-radius: 8px;
            padding: 15px;
            width: 320px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            font-size: 14px;
            line-height: 1.5;
            transition: opacity 0.2s ease, visibility 0.2s ease;
            z-index: 10;
        }

        .help-icon:hover .help-tooltip {
            visibility: visible;
            opacity: 1;
        }

        .results {
            width: 60%;
            margin: 60px auto;
            text-align: left;
        }

        .results p {
            color: #5f6368;
            font-size: 14px;
            margin-bottom: 20px;
        }

        .result-item {
            margin-bottom: 28px;
            background: white;
            border-radius: 8px;
            padding: 15px 20px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
            transition: transform 0.1s ease, box-shadow 0.1s ease;
        }

        .result-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }

        .result-item a {
            color: #1a0dab;
            text-decoration: none;
            font-size: 18px;
            font-weight: 500;
        }

        .result-item a:hover {
            text-decoration: underline;
        }

        .result-item .link {
            color: #006621;
            font-size: 13px;
            margin-bottom: 5px;
        }

        .result-item .snippet {
            color: #545454;
            font-size: 15px;
            margin-top: 5px;
            line-height: 1.5;
        }

        .pagination {
            text-align: center;
            margin-top: 20px;
            margin-bottom: 40px;
        }

        .pagination a {
            margin: 0 12px;
            text-decoration: none;
            color: #1a73e8;
            font-weight: 500;
        }

        .pagination a:hover {
            text-decoration: underline;
        }

        .document-view {
            width: 70%;
            margin: 40px auto;
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .document-view h2 {
            color: #1a73e8;
            margin-bottom: 10px;
            font-size: 24px;
        }

        .document-view .doc-path {
            color: #5f6368;
            font-size: 13px;
            margin-bottom: 20px;
        }

        .document-view .doc-content {
            color: #202124;
            font-size: 16px;
            line-height: 1.8;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .back-button {
            display: inline-block;
            padding: 10px 20px;
            background: #1a73e8;
            color: white;
            text-decoration: none;
            border-radius: 24px;
            font-weight: 500;
            margin-bottom: 20px;
            transition: background 0.2s ease;
        }

        .back-button:hover {
            background: #155ab6;
        }

    </style>
</head>
<body>
    <div class="search-container">
        <h1>Buscador</h1>
        <form action="{{ url_for('main.search') }}" method="get">
            <input type="text" name="q" value="{{ q|default('') }}" placeholder="Pesquise algo..." autocomplete="off">
            <button type="submit">Buscar</button>
            <div class="help-icon">?
                <div class="help-tooltip">
                    <b>Como fazer uma busca:</b><br><br>
                    Sua consulta pode ser uma <b>expressão Booleana</b> formada por palavras e conectores lógicos.<br><br>
                    Use <b>AND</b> para combinar termos e <b>OR</b> para incluir alternativas (em maiúsculas).<br>
                    Você também pode usar <b>parênteses</b> para alterar a precedência.<br><br>
                    <b>Exemplo:</b><br>
                    (<i>casa AND piscina</i>) OR praia
                </div>
            </div>
        </form>
    </div>
    {{ body|safe }}
</body>
</html>
"""

@main.route('/')
def index():
    return render_template_string(BASE_HTML, body="")

@main.route('/search')
def search():
    q = request.args.get('q', '').strip()
    page = int(request.args.get('page', '1') or 1)
    per_page = 10

    if not q:
        return render_template_string(BASE_HTML, q=q, body="")

    try:
        ast = parse_query(q)
    except Exception as e:
        return render_template_string(BASE_HTML, q=q, body=f"<div class='results'><p>Erro ao processar consulta: {e}</p></div>")

    query_terms = extract_terms(ast)
    index = current_app.indexer

    candidate_docs = docs_for_ast(index, ast)
    if not candidate_docs:
        return render_template_string(BASE_HTML, q=q, body=f"<div class='results'><p>Sem resultados para <b>{q}</b>.</p></div>")

    scores = score_docs(index, query_terms, candidate_docs)
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    total = len(sorted_docs)
    start = (page - 1) * per_page
    end = start + per_page
    page_docs = sorted_docs[start:end]

    results_html = "<div class='results'>"
    results_html += f"<p>Resultados {start+1}-{min(end,total)} de {total} para <b>{q}</b></p>"

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
        doc_url = url_for('main.view_document', doc_id=doc_id, q=q, page=page)
        
        # Remove a extensão .txt do título do link
        display_title = doc_id.replace('.txt', '') if doc_id.endswith('.txt') else doc_id

        results_html += f"""
        <div class="result-item">
            <div class="link">{doc_id}</div>
            <a href="{doc_url}">{display_title}</a><br>
            <div class="snippet">{snippet}</div>
        </div>
        """

    results_html += "</div>"

    nav = ""
    if start > 0:
        prev_url = url_for('main.search') + f"?q={q}&page={page-1}"
        nav += f'<a href="{prev_url}">&laquo; anterior</a> '
    if end < total:
        next_url = url_for('main.search') + f"?q={q}&page={page+1}"
        nav += f'<a href="{next_url}">próxima &raquo;</a>'
    if nav:
        results_html += f"<div class='pagination'>{nav}</div>"

    return render_template_string(BASE_HTML, q=q, body=results_html)

@main.route('/document/<path:doc_id>')
def view_document(doc_id):
    """Exibe o conteúdo completo de um documento."""
    index = current_app.indexer
    corpus_dir = current_app.corpus_dir
    
    # Parâmetros para voltar à busca
    q = request.args.get('q', '')
    page = request.args.get('page', '1')
    
    # Caminho completo do documento
    doc_path = os.path.join(corpus_dir, doc_id)
    
    # Verifica se o arquivo existe
    if not os.path.isfile(doc_path):
        error_html = f"""
        <div class="document-view">
            <a href="{url_for('main.search', q=q, page=page)}" class="back-button">← Voltar aos resultados</a>
            <h2>Documento não encontrado</h2>
            <p>O arquivo <code>{doc_id}</code> não foi encontrado.</p>
        </div>
        """
        return render_template_string(BASE_HTML, body=error_html)
    
    # Lê o conteúdo do documento
    try:
        with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        error_html = f"""
        <div class="document-view">
            <a href="{url_for('main.search', q=q, page=page)}" class="back-button">← Voltar aos resultados</a>
            <h2>Erro ao ler documento</h2>
            <p>Erro: {e}</p>
        </div>
        """
        return render_template_string(BASE_HTML, body=error_html)
    
    # Monta o HTML do documento
    doc_html = f"""
    <div class="document-view">
        <a href="{url_for('main.search', q=q, page=page)}" class="back-button">← Voltar aos resultados</a>
        <div class="doc-path">{doc_id}</div>
        <div class="doc-content">{content}</div>
    </div>
    """
    
    return render_template_string(BASE_HTML, body=doc_html)
    return render_template_string(BASE_HTML, q=q, body=results_html)
