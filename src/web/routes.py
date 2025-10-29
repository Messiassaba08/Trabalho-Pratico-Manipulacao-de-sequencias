from flask import Blueprint, request, render_template
from ..ri.search import perform_search

web_bp = Blueprint('web', __name__)

@web_bp.route('/', methods=['GET', 'POST'])
def search():
    results = []
    query = ''
    if request.method == 'POST':
        query = request.form.get('query')
        results = perform_search(query)
    return render_template('search.html', results=results, query=query)

@web_bp.route('/results', methods=['GET'])
def results():
    return render_template('results.html')