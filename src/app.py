from flask import Flask
from pathlib import Path

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_mapping(
        SECRET_KEY='your_secret_key',
        DATABASE='path_to_your_database',
    )

    # Initialize indexer before registering routes
    from indexer.inverted_index import InvertedIndex

    project_root = Path(__file__).resolve().parents[1]
    index_dir = project_root / 'data' / 'index'
    corpus_dir = project_root / 'data' / 'bbc'
    index_dir.mkdir(parents=True, exist_ok=True)
    index_path = index_dir / 'inverted_index.json'

    idx = InvertedIndex()
    idx.load_or_build(str(index_path), str(corpus_dir))
    app.indexer = idx
    app.corpus_dir = str(corpus_dir)

    # Register blueprints after indexer init
    from web.routes import main as web_routes
    app.register_blueprint(web_routes)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)