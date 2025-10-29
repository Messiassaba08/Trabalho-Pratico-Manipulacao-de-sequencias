bbc-search-engine
├── src
│ ├── app.py # Inicializa a aplicação Flask e define as configurações
│ ├── run.py # Ponto de entrada para executar a aplicação
│ ├── indexer # Módulo para indexação de documentos
│ │ ├── **init**.py # Marca o diretório indexer como um pacote
│ │ ├── trie.py # Implementa a estrutura de dados Trie
│ │ ├── inverted_index.py # Gerencia o índice invertido
│ │ └── persistence.py # Lida com o carregamento e salvamento do índice
│ ├── ri # Módulo para recuperação e ranqueamento
│ │ ├── **init**.py # Marca o diretório ri como um pacote
│ │ ├── query_parser.py # Analisa (parse) consultas Booleanas
│ │ ├── ranking.py # Contém funções para ranquear documentos
│ │ └── search.py # Lida com a lógica de busca
│ ├── web # Módulo para a interface web
│ │ ├── **init**.py # Marca o diretório web como um pacote
│ │ ├── routes.py # Define rotas para a aplicação web
│ │ ├── templates # Contém templates HTML
│ │ │ ├── base.html # Template HTML base
│ │ │ ├── search.html # Template da página de busca
│ │ │ └── results.html # Template da página de resultados
│ │ └── static # Contém arquivos estáticos (CSS, JS)
│ │ ├── css
│ │ │ └── style.css # Estilos CSS para a aplicação web
│ │ └── js
│ │ └── main.js # JavaScript para interatividade no lado do cliente
│ ├── utils # Funções utilitárias
│ │ ├── **init**.py # Marca o diretório utils como um pacote
│ │ ├── preprocessing.py # Funções para pré-processamento de dados de texto
│ │ └── snippets.py # Gera snippets (fragmentos) para exibir resultados
│ └── tests # Testes unitários para a aplicação
│ ├── test_trie.py # Testes para a implementação da Trie
│ ├── test_inverted_index.py # Testes para a implementação do InvertedIndex
│ └── test_query_parser.py # Testes para o analisador (parser) de consultas
├── data
│ ├── bbc # Arquivos brutos do corpus do dataset BBC News
│ ├── index # Diretório para armazenar o índice invertido
│ │ └── inverted_index.dat # Índice invertido serializado
├── docs # Documentação
│ └── report.md # Relatório final detalhando a implementação e descobertas
├── scripts # Scripts para construir (build) e servir a aplicação
│ ├── build_index.py # Constrói o índice invertido a partir dos arquivos brutos do corpus
│ └── serve.py # Inicia o servidor da aplicação Flask
├── requirements.txt # Lista as dependências necessárias para o projeto
├── .gitignore # Especifica arquivos e diretórios a serem ignorados pelo Git
└── README.md # Documentação para o projeto

## Clone o repositório

git clone <url-do-repositorio>
cd bbc-search-engine

## Instale as dependências necessárias

pip install -r requirements.txt

## Construa (build) o índice invertido

python scripts/build_index.py

## Execute a aplicação

python src/run.py

## Acesse a aplicação no seu navegador web em:

http://127.0.0.1:5000

## Uso

Use a barra de busca na página inicial para inserir sua consulta

Os resultados serão exibidos em uma página separada, mostrando documentos relevantes e snippets (fragmentos)
