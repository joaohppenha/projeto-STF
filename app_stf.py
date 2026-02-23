import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# Configuração da página - Tema e Layout
st.set_page_config(page_title="Analytics STF | Jurisprudência Estratégica", layout="wide")

# 1. Carregamento e Tratamento de Dados (Data Wrangling)
@st.cache_data
def carregar_dados():
    # Usando caminho relativo para garantir portabilidade no GitHub
    caminho_arquivo = "decisoes_stf_limpo.xlsx"
    
    if not os.path.exists(caminho_arquivo):
        st.error(f"Arquivo {caminho_arquivo} não encontrado no diretório local.")
        return pd.DataFrame()

    df = pd.read_excel(caminho_arquivo)
    
    # Seleção de features relevantes
    cols = ['nome_ministro', 'tempo_julgamento_dias', 'classe', 'ano da decisão', 
            'indicador_tramitacao', 'subgrupo andamento decisão', 'assuntos_processo']
    df = df[cols].copy()
    
    # Casting e Limpeza
    df['tempo_julgamento_dias'] = pd.to_numeric(df['tempo_julgamento_dias'], errors='coerce')
    df.dropna(subset=['nome_ministro', 'tempo_julgamento_dias'], inplace=True)
    
    return df

df_raw = carregar_dados()

if not df_raw.empty:
    # --- SIDEBAR: Filtros Inteligentes ---
    st.sidebar.header("Parâmetros de Análise")
    
    ministros = st.sidebar.multiselect(
        "Corpo Julgador:", 
        options=sorted(df_raw['nome_ministro'].unique()), 
        default=df_raw['nome_ministro'].unique()
    )
    
    classes = st.sidebar.multiselect(
        "Classe Processual:", 
        options=sorted(df_raw['classe'].dropna().unique()), 
        default=df_raw['classe'].dropna().unique()
    )
    
    # Slider com percentis para evitar que outliers extremos estraguem a escala
    min_val = int(df_raw['tempo_julgamento_dias'].min())
    max_val = int(df_raw['tempo_julgamento_dias'].max())
    
    tempo_range = st.sidebar.slider(
        "Janela de Tempo (Dias):",
        min_val, max_val, (min_val, 1000) # Default para focar no grosso das ações
    )

    # Aplicação dos Filtros
    mask = (
        df_raw['nome_ministro'].isin(ministros) & 
        df_raw['classe'].isin(classes) & 
        df_raw['tempo_julgamento_dias'].between(*tempo_range)
    )
    df = df_raw[mask]

    # --- HEADER: Títulos e KPIs ---
    st.title("⚖️ Analytics STF: Desempenho e Jurisprudência")
    st.markdown("### Diagnóstico Estatístico de Eficiência Processual")
    
    # Cálculos de Métricas
    total_acoes = len(df)
    mediana_tempo = df['tempo_julgamento_dias'].median()
    desvio_padrao = df['tempo_julgamento_dias'].std()
    taxa_decisao_final = (df["subgrupo andamento decisão"] == "DECISÃO FINAL").mean() * 100

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Volume Analisado", f"{total_acoes:,}")
    kpi2.metric("Mediana Lead Time", f"{mediana_tempo:.0f} dias", help="A mediana é mais robusta a outliers que a média.")
    kpi3.metric("Desvio Padrão", f"{desvio_padrao:.1f} d", help="Mede a variabilidade/imprevisibilidade dos julgamentos.")
    kpi4.metric("Taxa de Decisões Finais", f"{taxa_decisao_final:.1f}%")

    st.divider()

    # --- BODY: Visual Analytics ---
    col_left, col_right = st.columns(2)

    with col_left:
        # Gráfico 1: Boxplot (Fundamentação Estatística)
        st.subheader("Dispersão por Relatoria")
        fig_box = px.box(
            df, x="nome_ministro", y="tempo_julgamento_dias", 
            color="nome_ministro", points="outliers",
            title="Variabilidade do Tempo de Julgamento",
            labels={'tempo_julgamento_dias': 'Dias', 'nome_ministro': 'Ministro'}
        )
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    with col_right:
        # Gráfico 2: Pareto de Classes
        st.subheader("Concentração por Classe")
        df_classe = df['classe'].value_counts().reset_index()
        fig_pie = px.pie(
            df_classe, values='count', names='classe', 
            hole=.4, title="Distribuição de Demandas",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- SEÇÃO INFERIOR: Tabela de Eficiência Avançada ---
    st.subheader("Ranking de Eficiência Operacional")
    
    # Agrupamento Estatístico
    stats_ministro = df.groupby('nome_ministro').agg({
        'tempo_julgamento_dias': ['count', 'mean', 'median', 'std']
    }).reset_index()
    
    # Flattening nas colunas
    stats_ministro.columns = ['Ministro', 'Qtd Ações', 'Média Dias', 'Mediana Dias', 'Desvio Padrão']
    
    # Índice de Eficiência João (Normalizado: Ações por Tempo Médio)
    stats_ministro['Score Eficiência'] = (stats_ministro['Qtd Ações'] / stats_ministro['Mediana Dias']).round(4)
    stats_ministro = stats_ministro.sort_values(by='Score Eficiência', ascending=False)

    # Renderização com Gradiente
    st.dataframe(
        stats_ministro.style.background_gradient(subset=['Score Eficiência'], cmap='YlGn')
        .format(precision=2),
        use_container
