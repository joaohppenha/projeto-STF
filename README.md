# **<u>Projeto STF — Limpeza de Dados e Dashboard Interativo</u>**

## 1. Descrição do Projeto
Este projeto analisa decisões do STF a partir de dados públicos, realizando limpeza e padronização, e apresentando insights por meio de um dashboard interativo.

O projeto responde perguntas como:
- Qual o tempo médio de julgamento por ministro?
- Quantas decisões finais existem por classe?
- Qual ministro tem maior eficiência (mais decisões em menor tempo)?
- Quais padrões surgem ao longo dos anos?

---

## 2. Tecnologias e Conhecimentos Aplicados

### 2.1 Python
Conhecimentos aplicados:
- Leitura e escrita de arquivos (Excel)
- Manipulação de dados com DataFrames
- Tratamento de valores faltantes e padronização
- Criação de novas colunas e cálculos
- Controle de fluxo e validação de dados

### 2.2 Pandas
Conhecimentos aplicados:
- Leitura de dados (`read_excel`)
- Transformação e limpeza (normalização, conversão de tipos)
- Tratamento de duplicatas e valores nulos
- Criação de colunas calculadas (ex.: tempo de julgamento)
- Exportação de arquivo limpo (`to_excel`)

### 2.3 Streamlit
Conhecimentos aplicados:
- Construção de interface web simples e interativa
- Criação de filtros (multiselect, slider)
- Apresentação de métricas e cards
- Visualização de dados com gráficos interativos
- Exportação de dados em CSV via download

### 2.4 Plotly
Conhecimentos aplicados:
- Criação de gráficos interativos (barras, boxplot, pizza)
- Configuração de layout e estilos
- Manipulação de dados para visualização

### 2.5 TQDM
Conhecimentos aplicados:
- Barra de progresso em loops de processamento
- Melhor experiência durante o processamento de dados

### 2.6 Git
Conhecimentos aplicados:
- Versionamento de código
- Histórico de commits
- Organização do projeto em repositório

---

## 3. Projetos Incluídos

### Projeto 1 — Limpeza de Dados (Python)
O script realiza:
- leitura do arquivo Excel original
- padronização de colunas e valores
- conversão de datas
- criação de colunas calculadas (ex.: tempo de julgamento)
- remoção de duplicatas
- exportação do arquivo limpo

Saída: `decisoes_stf_limpo.xlsx`

---

### Projeto 2 — Dashboard Interativo (Streamlit)
O dashboard carrega o arquivo limpo e permite:
- filtros por ministro, classe e tempo de julgamento
- métricas e KPIs
- gráficos interativos (barras, boxplot, pizza)
- tabela de eficiência dos ministros
- download de CSV

---

## 4. Como Executar

### 4.1 Clonar o repositório

git clone https://github.com/joaohppenha/projeto-STF.git

### 4.2 Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

### 4.3 Instalar dependências
pip install -r requirements.txt

### 4.4 Executar a limpeza de dados
python limpeza_dados.py

### 4.5 Executar o dashboard
streamlit run dashboard_stf.py

## 5. Estrutura do Repositório
projeto-STF/
│
├── limpeza_dados.py
├── dashboard_stf.py
├── decisoes_STF.xlsx
├── decisoes_stf_limpo.xlsx
├── requirements.txt
└── README.md

## 6. Insights e Resultados

É possível analisar o tempo de julgamento por ministro e por classe.

O dashboard permite identificar:

quantidade de decisões finais por classe

participação de cada ministro

eficiência (decisões por tempo)

O projeto ajuda a visualizar padrões de desempenho e eficiência no STF.

## 7. Possíveis Melhorias

Adicionar filtros por ano e por assunto do processo.

Implementar análise de outliers no tempo de julgamento.

Criar comparação temporal por ano.

Publicar o dashboard online (Streamlit Cloud).

## 8. Observações

Os caminhos do arquivo são absolutos (ex.: C:\Users\...).
Para facilitar a execução em outros computadores, é recomendado usar caminhos relativos ou variáveis de ambiente.
cd projeto-STF

