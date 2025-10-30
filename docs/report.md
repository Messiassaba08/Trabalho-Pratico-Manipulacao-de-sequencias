Relatório sobre a Implementação do Mecanismo de Busca da BBC News
Introdução
Este documento descreve a implementação de um mecanismo de busca para o conjunto de dados (dataset) da BBC News, com foco na construção de um índice invertido usando uma estrutura de dados Trie (árvore de prefixos). O projeto visa fornecer recuperação eficiente de documentos com base em consultas booleanas, melhorando a experiência do usuário por meio de uma interface web construída com Flask.

Objetivos
Os objetivos principais deste projeto são:

Implementar uma estrutura de dados Trie para armazenar termos e seus documentos associados.

Criar um índice invertido que mapeia termos para IDs de documentos.

Desenvolver um módulo de busca capaz de processar consultas booleanas e classificar (rankear) os resultados com base na relevância.

Construir uma interface web amigável para consultar o conjunto de dados.

Detalhes da Implementação

1. Estrutura de Dados Trie
   A Trie é implementada em src/indexer/trie.py. Ela suporta inserção e busca eficientes de termos. Cada nó na Trie representa um caractere, e os caminhos através da Trie representam palavras. Essa estrutura permite pesquisas rápidas e é particularmente útil para recursos de autocompletar.

2. Índice Invertido
   O índice invertido é gerenciado em src/indexer/inverted_index.py. Este módulo associa termos a IDs de documentos, permitindo a recuperação rápida de documentos que contêm termos específicos. O índice é construído durante o processamento inicial do corpus da BBC News.

3. Persistência
   Para garantir que o índice invertido possa ser reutilizado entre sessões, a própria classe `InvertedIndex` (em `src/indexer/inverted_index.py`) lida com o salvamento e carregamento do índice em disco por meio dos métodos `save`, `load` e `load_or_build`. O índice é armazenado em **formato texto JSON** (arquivo `data/index/inverted_index.json`). Essa escolha privilegia legibilidade, interoperabilidade e depuração simples, além de atender ao requisito de não utilizar `pickle` nem serialização de objetos binários.

4. Processamento de Consultas
   O processamento de consultas é tratado em `src/ri/query_parser.py`, onde expressões booleanas são analisadas (parseadas) para uma AST com nós `Term`, `And` e `Or`. A execução da consulta e o ranqueamento são realizados em `src/ri/search.py`, que utiliza utilitários de `src/ri/ranking.py` para:
   - Determinar documentos candidatos via execução booleana sobre a AST (AND=interseção, OR=união);
   - Calcular a relevância de cada documento como a **média dos z-scores** dos termos da consulta.

5. Interface Web
   A aplicação web é construída usando Flask, com rotas definidas em src/web/routes.py. A interface permite aos usuários inserir consultas e visualizar os resultados. Os resultados são exibidos em formato paginado, com snippets (fragmentos) destacando os termos relevantes.

6. Testes
   Testes unitários são implementados no diretório src/tests para garantir a correção das funcionalidades da Trie, do índice invertido e do analisador (parser) de consultas. Esses testes validam que os componentes funcionam como esperado e lidam adequadamente com casos extremos (edge cases).

Conclusão
A implementação do mecanismo de busca da BBC News demonstra a aplicação prática de estruturas de dados e algoritmos na construção de uma aplicação web funcional. O uso de uma Trie para indexação e de um índice invertido para recuperação de documentos fornece uma solução robusta para pesquisar grandes conjuntos de dados. Trabalhos futuros podem incluir a melhoria do algoritmo de classificação (ranking) e a expansão da interface do usuário para melhor usabilidade.

Referências
Greene, D., & Cunningham, P. (2006). BBC News Dataset. Obtido em BBC News Dataset

Flask Documentation. Obtido em Flask
