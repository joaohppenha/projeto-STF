import pandas as pd
import os
from tqdm import tqdm

# Importa a Planilha de decisões do STF e verifica a existência do arquivo

arquivo_original = r'C:\Users\joaoh\OneDrive\Área de Trabalho\Projeto_STF\decisoes_STF.xlsx'

if not os.path.exists(arquivo_original):
    raise FileNotFoundError(f" Arquivo não encontrado: {arquivo_original}")

df = pd.read_excel(arquivo_original, engine='openpyxl')

##########################################################################################################################
# Limpeza de Dados
##########################################################################################################################

# Padronização

# Padronização de Nomes, Textos e Conversão de Datas
df.columns = df.columns.str.strip().str.lower()

colunas_texto = [
    'classe', 'nome ministro(a)', 'indicador eletrônico', 'indicador virtual', 
    'indicador colegiado', 'origem da decisão', 'subgrupo andamento decisão', 
    'andamento decisão', 'ramo direito', 'assuntos do processo', 
    'indicador de tramitação'
]

# barra de progresso
for c in tqdm(colunas_texto, desc="Padronizando colunas de texto"):
    if c in df.columns:
        df[c] = df[c].fillna('DESCONHECIDO').astype(str).str.strip().str.upper()
    else:
        print(f"Coluna '{c}' não encontrada. Criando com valor 'DESCONHECIDO'.")
        df[c] = 'DESCONHECIDO'

datas = ['data de autuação', 'data baixa', 'data da decisão']
for d in tqdm(datas, desc="Convertendo colunas de data"):
    if d in df.columns:
        df[d] = pd.to_datetime(df[d], errors='coerce')
    else:
        print(f"Coluna '{d}' não encontrada. Criando com NaT.")
        df[d] = pd.NaT


df = df.rename(columns={
    'nome ministro(a)': 'nome_ministro',
    'data de autuação': 'data_autuacao',
    'data baixa': 'data_baixa',
    'data da decisão': 'data_decisao',
    'origem da decisão': 'origem_decisao',
    'ramo direito': 'ramo_direito',
    'assuntos do processo': 'assuntos_processo',
    'indicador de tramitação': 'indicador_tramitacao'
})

# Criação de Colunas

if 'data_decisao' in df.columns:
    df['ano_decisao'] = df['data_decisao'].dt.year
else:
    df['ano_decisao'] = pd.NA

# Cálculo de tempo de julgamento
if all(col in df.columns for col in ['data_baixa', 'data_autuacao']):
    df['tempo_julgamento_dias'] = (df['data_baixa'] - df['data_autuacao']).dt.days
else:
    df['tempo_julgamento_dias'] = pd.NA

# Tratamento de Nulos (corrigido: usa pd.NA ao invés de None)
if 'tempo_julgamento_dias' in df.columns:
    df['tempo_julgamento_dias'] = df['tempo_julgamento_dias'].apply(
        lambda x: x if pd.notnull(x) and x >= 0 else pd.NA
    )

# Remoção de duplicatas
df = df.drop_duplicates()

# Conversão de colunas numéricas
numeric_cols = ['número', 'ano da decisão', 'qde de ocorrências processuais']
for col in tqdm(numeric_cols, desc="Convertendo colunas numéricas"):
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df['qde de ocorrências processuais'] = df['qde de ocorrências processuais'].fillna(0)


print(df.info())
print(df.head())
print(df['tempo_julgamento_dias'].describe())

# Exportar Novo Arquivo Limpo
arquivo_limpo = r'C:\Users\joaoh\OneDrive\Área de Trabalho\Projeto_STF\decisoes_stf_limpo.xlsx'

os.makedirs(os.path.dirname(arquivo_limpo), exist_ok=True)

df.to_excel(arquivo_limpo, index=False, engine='openpyxl')

print(f"\n Arquivo limpo salvo com sucesso em: {arquivo_limpo}")

input()
