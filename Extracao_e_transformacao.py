import pandas as pd
import os
from tqdm import tqdm
import numpy as np

def limpar_dados_stf():
    # 1. Configuração de Caminhos (Portabilidade para GitHub/Produção)
    # Busca o arquivo no diretório atual do script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    arquivo_original = os.path.join(diretorio_atual, 'decisoes_STF.xlsx')
    arquivo_limpo = os.path.join(diretorio_atual, 'decisoes_stf_limpo.xlsx')

    print(f"Iniciando Pipeline de Preprocessamento...")
    
    if not os.path.exists(arquivo_original):
        print(f"ERRO: O arquivo {arquivo_original} nao foi encontrado.")
        return

    # 2. Carga de Dados
    print("Carregando base de dados (Excel)...")
    df = pd.read_excel(arquivo_original, engine='openpyxl')

    # 3. Padronização de Schema (Colunas)
    df.columns = df.columns.str.strip().str.lower()

    # Dicionário de Renomeação para legibilidade (Snake Case)
    rename_dict = {
        'nome ministro(a)': 'nome_ministro',
        'data de autuação': 'data_autuacao',
        'data baixa': 'data_baixa',
        'data da decisão': 'data_decisao',
        'origem da decisão': 'origem_decisao',
        'ramo direito': 'ramo_direito',
        'assuntos do processo': 'assuntos_processo',
        'indicador de tramitação': 'indicador_tramitacao',
        'ano da decisão': 'ano_da_decisao'
    }
    df = df.rename(columns=rename_dict)

    # 4. Processamento de Texto (Data Cleaning)
    colunas_texto = [
        'classe', 'nome_ministro', 'origem_decisao', 'subgrupo andamento decisão', 
        'andamento decisão', 'ramo_direito', 'assuntos_processo', 'indicador_tramitacao'
    ]

    for c in tqdm(colunas_texto, desc="Limpando strings"):
        if c in df.columns:
            # Preenche nulos, converte para string, limpa espaços e coloca em caixa alta
            df[c] = df[c].fillna('DESCONHECIDO').astype(str).str.strip().str.upper()

    # 5. Processamento de Datas (Temporal Analysis)
    datas = ['data_autuacao', 'data_baixa', 'data_decisao']
    for d in tqdm(datas, desc="Formatando datas"):
        if d in df.columns:
            df[d] = pd.to_datetime(df[d], errors='coerce')

    # 6. Feature Engineering (Cálculo de Lead Time e Ano)
    print("Gerando novas features...")
    
    # Extração do ano da decisão
    if 'data_decisao' in df.columns:
        df['ano_decisao_extraido'] = df['data_decisao'].dt.year

    # Cálculo do tempo de julgamento em dias
    if 'data_baixa' in df.columns and 'data_autuacao' in df.columns:
        df['tempo_julgamento_dias'] = (df['data_baixa'] - df['data_autuacao']).dt.days
        
        # Tratamento de inconsistências: tempos negativos viram nulos
        df.loc[df['tempo_julgamento_dias'] < 0, 'tempo_julgamento_dias'] = np.nan

    # 7. Conversão Numérica e Tipagem
    numeric_cols = ['número', 'ano_da_decisao', 'qde de ocorrências processuais']
    for col in tqdm(numeric_cols, desc="Corrigindo tipos numericos"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 8. Finalização (Deduplicação e Exportação)
    print("Finalizando processamento...")
    df = df.drop_duplicates()
    
    # Ordenação lógica (Ministro e Data)
    if 'nome_ministro' in df.columns and 'data_decisao' in df.columns:
        df = df.sort_values(by=['nome_ministro', 'data_decisao'])

    # Salvando a base processada
    df.to_excel(arquivo_limpo, index=False, engine='openpyxl')
    
    print("-" * 30)
    print(f"Pipeline concluido com sucesso!")
    print(f"Registros processados: {len(df)}")
    print(f"Arquivo salvo: {arquivo_limpo}")
    print("-" * 30)

if __name__ == "__main__":
    limpar_dados_stf()
    input("\nPressione Enter para sair...")
