# Analise de Eficiencia Jurisprudencial — STF

## 1. Descricao do Projeto
Este projeto aplica tecnicas de Ciencia de Dados e Analytics sobre dados publicos do Supremo Tribunal Federal (STF) para diagnosticar a performance processual da corte. Atraves de um pipeline de Data Wrangling em Python e um dashboard interativo desenvolvido em Streamlit, o projeto transforma dados brutos em inteligencia estrategica, permitindo a analise de gargalos operacionais e padroes de julgamento.

O projeto responde a perguntas criticas de negocio e gestao, tais como:
* Qual o lead time (tempo medio de julgamento) segregado por Ministro?
* Qual a distribuicao de decisoes finais por classe processual?
* Quais Ministros apresentam maior eficiencia relativa (volume de decisoes vs. tempo)?
* Quais padroes de produtividade emergem na serie historica analisada?

## 2. Tecnologias e Metodologias Aplicadas

### 2.1 Python e Data Wrangling (Pandas)
* Manipulacao de datasets complexos e tratamento de inconsistencias em dados juridicos.
* Preprocessamento e normalizacao de registros e conversao de tipos de dados.
* Feature Engineering: Criacao de metricas derivadas, como o calculo de tempo transcorrido ate o julgamento.
* Higienizacao de valores ausentes (NaN) e remocao de duplicatas para garantia da integridade analitica.

### 2.2 Visual Analytics (Streamlit e Plotly)
* Desenvolvimento de Data App para apresentacao de resultados em tempo real.
* Implementacao de filtros dinamicos (multiselect e sliders) para exploracao granular dos dados.
* Utilizacao de graficos interativos e analise de dispersao (Boxplots) para identificacao de outliers no tempo de julgamento.
* Monitoramento de KPIs atraves de metricas e indicadores de performance.

### 2.3 Engenharia e Boas Praticas
* Versionamento de codigo utilizando Git.
* Gerenciamento de dependencias e ambientes virtuais (venv).
* Otimizacao de processamento com feedback visual via TQDM.

## 3. Estrutura do Pipeline

### Fase 1: ETL e Limpeza (limpeza_dados.py)
O script automatiza a leitura da base original, executa a padronizacao de colunas e valores, realiza o parsing de datas e exporta um dataset otimizado para consumo analitico (decisoes_stf_limpo.xlsx).

### Fase 2: Business Intelligence (dashboard_stf.py)
Interface que consome o dado processado e permite a exploracao de insights, tabelas de eficiencia e visualizacoes estatisticas avançadas.

## 4. Como Executar

### 4.1 Clonar o repositorio
git clone https://github.com/joaohppenha/projeto-STF.git

### 4.2 Configurar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

### 4.3 Instalar dependencias
pip install -r requirements.txt

### 4.4 Executar o processamento e o dashboard
python limpeza_dados.py
streamlit run dashboard_stf.py

## 5. Estrutura do Repositorio
projeto-STF/
├── limpeza_dados.py          # Script de processamento e ETL
├── dashboard_stf.py          # Aplicacao Streamlit
├── decisoes_STF.xlsx         # Raw Data (Dados Brutos)
├── decisoes_stf_limpo.xlsx   # Processed Data (Dados Limpos)
├── requirements.txt          # Dependencias do projeto
└── README.md                 # Documentacao

## 6. Insights e Resultados Obtidos
A analise permite identificar disparidades no tempo de julgamento entre diferentes classes processuais e perfis de produtividade por relatoria. A ferramenta serve como suporte para diagnosticos de eficiencia juridica, permitindo identificar quais classes demandam maior tempo de analise e como a carga de trabalho esta distribuida entre os Ministros.

## 7. Proximas Etapas e Escalabilidade
* Implementacao de analise preditiva para estimativa de desfechos baseada em series historicas.
* Migracao do armazenamento de arquivos Excel para Banco de Dados Relacional (PostgreSQL).
* Deploy da aplicacao em ambiente Cloud (Streamlit Cloud ou AWS).
