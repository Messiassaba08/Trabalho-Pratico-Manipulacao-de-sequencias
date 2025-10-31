# BBC Search — Guia Rápido

Aplicação web em Flask para buscar no corpus BBC (data/bbc). Este guia traz só o essencial para instalar e rodar.

## Requisitos

- Python 3.8+

## Instalação

```
pip install -r requirements.txt
```

## Construir índice (opcional)

```
python scripts/build_index.py
```

Se o arquivo `data/index/inverted_index.json` não existir, ele será criado automaticamente no primeiro run.

## Executar

```
python src/run.py
```

Acesse: http://127.0.0.1:5000

## Uso rápido

- Digite termos na busca. Suporta `AND`, `OR` e parênteses.
- Ex.: `home AND england` ou `(economy OR market) AND business`.

## Estrutura do projeto (resumo)

```
src/
	app.py
	run.py
	indexer/
		inverted_index.py
		trie.py
		persistence.py
	ri/
		query_parser.py
		ranking.py
		search.py
	web/
		routes.py
		templates/
			base.html
			search.html
			results.html
	utils/
		preprocessing.py
		snippets.py
	tests/
scripts/
	build_index.py
	serve.py
data/
	bbc/
	index/
		inverted_index.json
docs/
	report.md
```
